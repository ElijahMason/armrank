#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

async function openDb(dbPath){
	const initSqlJs = require('sql.js');
	const SQL = await initSqlJs();
	const filebuffer = fs.readFileSync(dbPath);
	return new SQL.Database(filebuffer);
}

function rowToObj(columns, row){
	const obj = {};
	columns.forEach((c, i)=>{ obj[c] = row[i]; });
	return obj;
}

function queryAll(db, sql, params=[]){
	const stmt = db.prepare(sql);
	stmt.bind(params);
	const cols = stmt.getColumnNames();
	const out = [];
	while(stmt.step()){
		const row = stmt.get();
		out.push(rowToObj(cols, row));
	}
	stmt.free();
	return out;
}

function printTable(rows){
	if(rows.length === 0){ console.log('No rows'); return }
	const keys = Object.keys(rows[0]);
	console.log(keys.join('\t'));
	for(const r of rows){
		console.log(keys.map(k=>String(r[k] ?? '')).join('\t'));
	}
}

function normalizeHand(v){
	if(!v) return null;
	const s = String(v).trim().toUpperCase();
	if(['R','RIGHT','RH'].includes(s)) return 'RH';
	if(['L','LEFT','LH'].includes(s)) return 'LH';
	return s;
}

async function main(){
	const args = require('minimist')(process.argv.slice(2));
	const cmd = args._[0];
	const dbPath = args.db || path.join(__dirname, 'data', 'ratings.db');
	if(!fs.existsSync(dbPath)){
		console.error('DB not found:', dbPath);
		process.exit(1);
	}
	const db = await openDb(dbPath);
	if(cmd === 'ratings'){
		const hand = normalizeHand(args.hand) || null;
		const conds = [];
		const params = [];
		if(hand){ conds.push('r.context_hand = ?'); params.push(hand) }
		const where = conds.length ? ('WHERE ' + conds.join(' AND ')) : '';
		const rows = queryAll(db, `
			SELECT p.name, r.context_hand AS hand, r.mu, r.sigma, (r.mu - 3*r.sigma) AS conservative, r.updated_at
			FROM ratings r JOIN players p ON p.id = r.player_id
			${where}
			ORDER BY conservative DESC
		`, params);
		printTable(rows);
	}else if(cmd === 'events'){
		const limit = Number(args.limit || 20);
		const rows = queryAll(db, `
			SELECT id, event_type, name, date, context_hand
			FROM events ORDER BY id DESC LIMIT ?
		`, [limit]);
		printTable(rows);
	}else if(cmd === 'player'){
		const name = args.name;
		if(!name){ console.error('--name is required'); process.exit(1) }
		const idRows = queryAll(db, 'SELECT id, name, sex, weight FROM players WHERE name = ? COLLATE NOCASE', [name]);
		if(idRows.length === 0){ console.log('Player not found'); process.exit(0) }
		const pid = idRows[0].id;
		console.log('Player\t' + idRows[0].name + '\tSex\t' + (idRows[0].sex || '') + '\tWeight\t' + (idRows[0].weight || ''));
		console.log('\nRatings:');
		printTable(queryAll(db, `
			SELECT context_hand AS hand, mu, sigma, (mu - 3*sigma) AS conservative, updated_at
			FROM ratings WHERE player_id = ? ORDER BY updated_at DESC
		`, [pid]));
		console.log('\nEvents:');
		const sm = queryAll(db, `
			SELECT e.id, 'supermatch' AS type, e.name, e.date FROM events e
			JOIN supermatches s ON s.event_id = e.id
			WHERE s.a_player_id = ? OR s.b_player_id = ?
			ORDER BY e.id DESC
		`, [pid, pid]);
		const tr = queryAll(db, `
			SELECT e.id, 'tournament' AS type, e.name, e.date, t.placement FROM events e
			JOIN tournament_results t ON t.event_id = e.id
			WHERE t.player_id = ?
			ORDER BY e.id DESC
		`, [pid]);
		printTable([...sm, ...tr]);
	}else{
		console.log('Usage: node backend/query.js <ratings|events|player> [--db path] [--hand RH|LH]');
		process.exit(1);
	}
}

main().catch(err=>{ console.error(err); process.exit(1) }); 