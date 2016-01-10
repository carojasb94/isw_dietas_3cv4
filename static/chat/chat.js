/**
 * Created by metallica on 6/01/16.
 */



/**
 * Created by metallica on 10/12/15.

var canal = document.getElementById("canal");
console.log(slug_empresa);
console.log(slug_empresa.getAttribute("value"));


 */

swampdragon.ready(function () {
    console.log("FUNCION READY SWAMPDRAGON-KARUSSA");
    //swampdragon.subscribe('notifications', 'notifications', null);
    var canal = slug_empresa.getAttribute("value") || 'sin-empresa';
    swampdragon.subscribe('karussa_notificaciones', canal, {'slug_empresa': slug_empresa.getAttribute("value") || ""});
    console.log("se subscribio al canal "+canal+" -karussa");

    nueva_notificacion("se subscribio al canal "+canal+" -karussa");

});


window.addEventListener('load', function () {
    Notification.requestPermission(function (status) {
        console.log("addEventListener -karussa");
        console.log(status);
        // This allows to use Notification.permission with Chrome/Safari
        if (Notification.permission !== status) {
            console.log(status+" dentro del if -karussa");
            Notification.permission = status;
        }
    });
});


// Esta a la escucha de cada mensaje enviado desde el router a la vista
swampdragon.onChannelMessage(function (channels, message) {
    console.log("onChanelMessage-karussa");
    console.log(channels);
    console.log(message);

    if (message.action === "created") {
        addNotification((message.data));
    }
});


function nueva_notificacion(mensaje) {
    // Si el usuario autorizo mostrar las notificaciones, se crea la notificacion con el mensaje
    if (window.Notification && Notification.permission === "granted") {
        console.log('Tiene permisos para notificaciones');
        randomNotification(mensaje);
    }
}

// Add new notifications
function addNotification(notification) {
    // Si el usuario autorizo mostrar las notificaciones, se crea la notificacion con el mensaje
    if (window.Notification && Notification.permission === "granted") {
        console.log('Tiene permisos para notificaciones');
        new Notification(notification.message);

    }

    /*
    // Add the new notification
    var li = document.createElement("li");
    li.innerHTML = notification.message;
    console.log("lista de notificaciones ");
    console.log(notificationsList);
    notificationsList.insertBefore(li, notificationsList.firstChild);

    // Remove excess notifications
    while (notificationsList.getElementsByTagName("li").length > 5) {
        notificationsList.getElementsByTagName("li")[5].remove();
    }
    */
}


/*
function notifyMe() {
  // Let's check if the browser supports notifications
  if (!("Notification" in window)) {
    alert("This browser does not support system notifications");
  }

  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === "granted") {
    // If it's okay let's create a notification
    var notification = new Notification("Hi there!");
  }

  // Otherwise, we need to ask the user for permission
  else if (Notification.permission !== 'denied') {
    Notification.requestPermission(function (permission) {
      // If the user accepts, let's create a notification
      if (permission === "granted") {
        var notification = new Notification("Hi there!");
      }
    });
  }

  // Finally, if the user has denied notifications and you
  // want to be respectful there is no need to bother them any more.
}
*/

function spawnNotification(theBody, theIcon, theTitle) {
    var options = {
        body: theBody,
        icon: theIcon
    };
    var n = new Notification(theTitle, options);
    setTimeout(n.close.bind(n), 5000);
}


function abrir_video()
{
    newwindow=window.open('https://www.somosrenka.com','pop-up por click en Notificacion','height=200,width=150');
    if (window.focus) {
        newwindow.focus();
    }
    return false;
}

function randomNotification(mensaje) {
    console.log('random notification');
    var options = {
        body: mensaje,
        icon: '/static/base/img/frida_30x30.jpg'
    };
    console.log(options);
    var opciones = {
        body: mensaje,
        icon: '/static/base/img/frida_30x30.jpg',
        onclick: 'https://www.somosrenka.com'
    };
    var n1 = new Notification('Karussa Yoga', {body:mensaje});
    var n2 = new Notification('Karussa Yoga',{ icon: '/static/base/img/frida_30x30.jpg' });
    var n3 = new Notification('Karussa Yoga', opciones);
    console.log(n1);
    console.log(n2);
    console.log(n3);
    //setTimeout(n.close.bind(n), 5000);
}





