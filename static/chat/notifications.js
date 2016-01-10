// Ask the browser for permission to show notifications
// Taken from https://developer.mozilla.org/en-US/docs/Web/API/Notification/Using_Web_Notifications
window.addEventListener('load', function () {
    Notification.requestPermission(function (status) {
        console.log("addEventListener");
        console.log(status);
        // This allows to use Notification.permission with Chrome/Safari
        if (Notification.permission !== status) {
            console.log(status+" dentro del if");
            Notification.permission = status;
        }
    });
});


// Subscribe once swampdragon is connected
swampdragon.open(function () {
        console.log("open");
    swampdragon.subscribe('notifications', 'mensajes_eds');

});

// This is the list of notifications
var notificationsList = document.getElementById("notifications");

// New channel message received
swampdragon.onChannelMessage(function (channels, message) {
    // Add the notification
    console.log("onChanelMessage");
    console.log(channels);
    console.log(message);
    console.log(message.data);
    console.log(message.data.img);
    console.log(message.data.message);

    if (message.action === "created") {
        addNotification((message.data));
    }
});



// Add new notifications
function addNotification(notification) {
    // If we have permission to show browser notifications
    // we can show the notifiaction
    if (window.Notification && Notification.permission === "granted") {
        new Notification(notification.message);
    }

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
}
