// Referencias a los elementos
const navbar = document.getElementById('navbar');
const darkModeToggle = document.getElementById('dark-mode-toggle');
const darkModeIcon = document.getElementById('dark-mode-icon');
const body = document.body;
const logo = document.getElementById('logo');
const loginSection = document.getElementById('login-section');

// Simulación de login
let isLoggedIn = false;

// Controlar el fondo del navbar en scroll
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// Cambiar entre modos claro/oscuro
darkModeToggle.addEventListener('click', () => {
    if (body.classList.contains('dark-mode')) {
      body.classList.remove('dark-mode');
      body.classList.add('light-mode');
      darkModeIcon.classList.replace('bx-moon', 'bx-sun'); // Cambia a sol
    } else {
      body.classList.remove('light-mode');
      body.classList.add('dark-mode');
      darkModeIcon.classList.replace('bx-sun', 'bx-moon'); // Cambia a luna
    }
  });

// Redirigir al inicio al presionar el logo
logo.addEventListener('click', () => {
  window.location.href = '/'; // Cambia '/' por la URL de tu página de inicio
});

// Control de Login
if (isLoggedIn) {
  loginSection.style.display = 'none';
}




// Slide
// Referencias a los elementos
const sidebar = document.querySelector('.sidebar');
const toggleBtn = document.querySelector('#toggle-sidebar');
let sidebarVisible = true; // Por defecto, la barra está visible
// Evento para alternar la barra
toggleBtn.addEventListener('click', toggleSidebar);
// Función para alternar la barra
function toggleSidebar() {
  sidebarVisible = !sidebarVisible;

  if (sidebarVisible) {
    sidebar.classList.remove('sidebar-hidden');
    toggleBtn.style.right = '+400px'; // Mueve el botón junto con la barra
    toggleBtn.innerHTML = "<i class='bx bx-chevron-right'></i>"; // Icono para cerrar
  } else {
    sidebar.classList.add('sidebar-hidden');
    toggleBtn.style.right = '-5px'; 
    toggleBtn.innerHTML = "<i class='bx bx-chevron-left'></i>"; // Icono para abrir
  }
}



// Función para generar la representación de estrellas
function generarEstrellas(calificacion) {
  // Contenedor de estrellas vacías (fondo gris)
  let estrellasHTML = "<span class='estrellas'><span class='estrellas-fondo'>";
  for (let i = 0; i < 5; i++) {
      estrellasHTML += "<i class='bx bxs-star'></i>"; // Estrella vacía
  }
  estrellasHTML += "</span>";

  // Contenedor de estrellas llenas (fondo amarillo) con ancho limitado
  estrellasHTML += "<span class='estrellas-fraccion' style='width:" + (calificacion / 5) * 100 + "%'>";
  for (let i = 0; i < 5; i++) {
      estrellasHTML += "<i class='bx bxs-star'></i>"; // Estrella llena
  }
  estrellasHTML += "</span></span>";

  return estrellasHTML;
}


/*Calificar*/
function submitCalificacion(tipo, tipo_id) {
  var formData = new FormData(document.getElementById('calificacion-form'));

  formData.append('tipo', tipo);
  formData.append('tipo_id', tipo_id);

  fetch('/calificar/', {
      method: 'POST',
      body: formData,
      headers: {
          'X-CSRFToken': getCookie('csrftoken')
      }
  }).then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            /*document.getElementById('popup-details').style.display = 'none';*/
            location.reload();
            alert('Gracias por su opinión. :)');
        } else {
            alert('Error: ' + data.message);
        }
    });
}


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


/*Favoritos*/
// Delegación de eventos en el contenedor
document.body.addEventListener('click', function (event) {
  if (event.target.closest('.favorite-btn')) {
      const button = event.target.closest('.favorite-btn');
      const id = button.getAttribute('data-id');
      const tipo = button.getAttribute('data-tipo');

      fetch('/toggle_favorito/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ id, tipo })
      })
      .then(response => response.json())
      .then(data => {
          if (data.status === 'added') {
              button.classList.remove('btn-outline-primary');
              button.classList.add('btn-primary');
              button.innerHTML = '<i class="bx bxs-star"></i> Favorito';
          } else if (data.status === 'removed') {
              button.classList.remove('btn-primary');
              button.classList.add('btn-outline-primary');
              button.innerHTML = '<i class="bx bx-star"></i> Marcar como Favorito';
          }
          
      })
      .catch(error => console.error('Error:', error));
  }
});
