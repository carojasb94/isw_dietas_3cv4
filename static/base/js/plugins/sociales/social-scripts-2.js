



        // recuperar contidad de likes/compartidos
        //$('#btn-shares').on('click', likes);
        function likes(host , path_actual)
        {
            //console.log('funcion activada por el boton like');
            $.ajax
            ({
                url: 'https://graph.facebook.com/?id='+host+path_actual,
                type: 'get',
                success: function (result) {
                    //console.log(result);
                    if (!result || result == 1) {
                        console.log("Ningun compartido");
                    }
                    //console.log(result['shares']);
                    var html = result['shares'];
                    console.log(html);
                    $('#fb-share-count').html(html);
                }
            });
        }

        function twetts(host , path_actual)
        {
            //console.log('funcion activada por el boton like');
            $.ajax
            ({
                url: 'https://graph.facebook.com/?id='+host+path_actual,
                type: 'get',
                success: function (result) {
                    //console.log(result);
                    if (!result || result == 1) {
                        console.log("Ningun compartido");
                    }
                    //console.log(result['shares']);
                    var html = result['shares'];
                    console.log(html);
                    $('#fb-share-count').html(html);
                }
            });
        }

/*
    $(document).ready(function() {
    url = "http://www.somosrenka.com/";
    beforecounter = " <b>";
    aftercounter = "</b>";

    // Get Number of Facebook Shares
    $.getJSON('http://graph.facebook.com/'+url+'&callback=?',
        function(data) {
            $('#facebook').append(beforecounter + data.shares + aftercounter);
    });

    // Get Number of Tweet Count
    $.getJSON('http://urls.api.twitter.com/1/urls/count.json?url='+url+'&callback=?',
        function(data) {
            $('#twitter').append(beforecounter + data.count + aftercounter);
    });

});
*/

    function pblic(direccion,imagen) {
        var publish = {
            method: 'feed',
            message: 'testeando compartir',
            name: 'NOmbre de mi cosa a compartir ',
            caption: 'Caption',
            description: (
            'Descripcion para lo que se compartira en fb.'
            ),
            link: 'http://localhost:8000/media/usuarios/19/vegano_user.jpg',
            picture: 'http://localhost:8000/media/usuarios/19/vegano_user.jpg',
            actions: [
                {name: 'NOmbre_action', link: 'http://localhost:8000/media/usuarios/19/vegano_user.jpg'}
            ],
            properties: [
                {text: 'value1', href: 'http://developers.facebook.com/'},
                {text: 'value1', href: 'http://developers.facebook.com/'},
                {text: 'value1', href: 'http://developers.facebook.com/'},
                {text: 'value1', href: 'http://developers.facebook.com/'},
                {text: 'value1', href: 'http://developers.facebook.com/'}
            ],
            user_message_prompt: 'Share your thoughts about RELL'
        };
        FB.ui(publish, info.bind('feed callback'));
    }


        // Funcion para Compartir
        function compartir() {
            FB.ui(
                    {
                        method: 'feed',
                        name: "{{ proyecto.nombre }}",
                        link: "http://localhost:8000/media/usuarios/19/vegano_user.jpg",
                        picture: "http://localhost:8000/media/usuarios/19/vegano_user.jpg",
                        caption: 'www.Somosrenka.com Invierte y Apoya Proyectos',
                        description: "{{ proyecto.descripcion }}",
                        message: "Apoyemos el proyecto {{ proyecto.descripcion }}..."
                    },
                    function (response) {
                        if (response && response.post_id) {
                            alert('Post Publicado.');
                        }
                    }
            );
        }

            function stream() {
        FB.ui({
                    method: 'stream.share',
                    u: 'http://localhost:8000/media/usuarios/19/vegano_user.jpg'
                },
                function (response) {
                    alert(response);
                }
        );
    };


        function opengraf() {
            FB.ui({
                method: 'share_open_graph',
                action_type: 'og.likes',

                action_properties: JSON.stringify({
                    object: 'http://localhost:8000/proyectos/7'
                })
            }, function (response) {
                console.log(response); });
            // action_type: 'matchadviceuk:share',    // appNameSpace:myCustomAction

        }


        $(function () {
            FB.init({
                appId: 'APP_ID',
                status: true, // check login status
                cookie: true, // enable cookies to allow the server to access the session
                xfbml: true  // parse XFBML
            });

            FB.getLoginStatus(function (response) {
                if (response.status == 'connected') {
                    getCurrentUserInfo(response)
                } else {
                    FB.login(function (response) {
                        if (response.authResponse) {
                            getCurrentUserInfo(response)
                        } else {
                            console.log('Auth cancelled.')
                        }
                    }, {scope: 'email'});
                }
            });

            function getCurrentUserInfo() {
                FB.api('/me', function (userInfo) {
                    console.log(userInfo.name + ': ' + userInfo.email);
                });
            }
        });
