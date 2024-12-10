// ICONS
let uIcon = L.icon({
    iconUrl: '/media/marker/universityS.png',  
    iconSize: [55, 55],  
    iconAnchor: [25, 45],  
    popupAnchor: [0, -40], 
});
let uIconP = L.icon({
    iconUrl: '/media/marker/universityP.png',  
    iconSize: [50, 55],  
    iconAnchor: [25, 45],  
    popupAnchor: [0, -40], 
});
let fIcon = L.icon({
    iconUrl: '/media/marker/facultyS.png',  
    iconSize: [55, 55], 
    iconAnchor: [25, 45], 
    popupAnchor: [0, -40] 
});
let fIconP = L.icon({
    iconUrl: '/media/marker/facultyP.png',  
    iconSize: [55, 55],  
    iconAnchor: [25, 45],  
    popupAnchor: [0, -40]  
});

let cIcon = L.icon({
    iconUrl: '/media/marker/carreraS.png',  
    iconSize: [55, 55],  
    iconAnchor: [25, 45],  
    popupAnchor: [0, -40]  
});
let cIconP = L.icon({
    iconUrl: '/media/marker/carreraP.png',  
    iconSize: [55, 55],  
    iconAnchor: [25, 45],  
    popupAnchor: [0, -40]  
});



// Función para abrir todos los popups de una capa
function openPopups(layerGroup) {
    layerGroup.eachLayer(function(layer) {
        if (layer instanceof L.Marker) {
            layer.openPopup(); // Abre el popup para cada marcador
        }
    });
  }



