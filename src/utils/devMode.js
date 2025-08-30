export function isDevMode(){
  try{
    const host = String(window?.location?.host || '').toLowerCase()
    // Treat beta deployment as dev mode per requirements
    return host.includes('beta.armrank.net')
  }catch(e){ return false }
}

