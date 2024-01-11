const button=document.querySelector(".b");

button.addEventListener("click",()=>{
    navigator.geolocation.getCurrentPosition(position=>{
        const {latitude,longitude}=position.coords;
        console.log(latitude+" "+latitude);
        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`;
        fetch(url).then(res=>res.json()).then(data=>{
            console.table(data.address);
        }).catch(()=>{
            console.log("Error fetching data from API");
        })
    })
});
$('#addAddressModal1').on('shown.bs.modal', function () {
    initMap();
});
let map;

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");

    map = new Map(document.getElementById("map"), {
        center: { lat: 28.70, lng: 77.10 },
        zoom: 15,
    });
    new google.maps.Marker({
        position:{ lat: 28.70, lng: 77.10 },
        map:map,
        label:"A",
        title:"New Delhi",
        animation:google.maps.Animation.BOUNCE
    })
}