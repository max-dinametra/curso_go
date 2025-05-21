document.addEventListener('DOMcontentLoaded', async () => {
//fetch the publishable keys and init stripe
const {publishableKey} = await fetch("/config").then(r => r.json())


//Fetch the payment intents clients secret


//mount the Elements

})