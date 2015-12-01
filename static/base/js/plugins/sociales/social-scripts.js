function autoscape(selector) {
    return selector.replace(/(!|"|#|\$|%|\'|\(|\)|\*|\+|\,|\.|\/|\:|\;|\?|@)/g, function ($1, $2) {
        return "\\\\" + $2;
    });
}


function openFbPopUp(host, request_path, nombre_proyecto, descripcion_proyecto, imagen_url, id_proyecto, actualizacion) {
    social_counter(id_proyecto, "facebook", actualizacion);

    var fburl = host + request_path;
    var fbimgurl = host + '/' + imagen_url;
    var fbtitle = nombre_proyecto;
    var fbsummary = descripcion_proyecto;
    if (fbimgurl == '') {
        var sharerURL = "http://www.facebook.com/sharer/sharer.php?s=100&p[url]=" + encodeURI(fburl) + "&p[title]=" + encodeURI(fbtitle) + "&p[summary]=" + encodeURI(fbsummary);

    }
    else {
        var sharerURL = "http://www.facebook.com/sharer/sharer.php?s=100&p[url]=" + encodeURI(fburl) + "&p[images][0]=" + encodeURI(fbimgurl) + "&p[title]=" + encodeURI(fbtitle) + "&p[summary]=" + encodeURI(fbsummary);

    }

    window.open(sharerURL,
        'facebook-share-dialog',
        'width=626,height=436');
    return false;
}

function openLkInPopUp(host, request_path, nombre_proyecto, descripcion_proyecto, imagen_url, id_proyecto, actualizacion) {
    //console.log("PopUp linkedin");
    social_counter(id_proyecto, "linkedin", actualizacion);

    var lkurl = host + request_path;
    var lkimgurl = host + '/' + imagen_url;
    var lktitle = nombre_proyecto;
    var lksummary = descripcion_proyecto;
    var lkhost = host;
    var sharerURL = "http://www.linkedin.com/shareArticle?mini=true&url=" + encodeURI(lkurl) + "&title=" + encodeURI(lktitle) + "&summary=" + encodeURI(lksummary) + "&source=" + encodeURI(lkhost);
    //console.log(sharerURL);
    window.open(
        sharerURL,
        'linkedin-share-dialog',
        'width=626,height=436');
    return false;
}

/////////////////////////////////////////
function opentwPopUp(host, request_path, nombre_proyecto, descripcion_proyecto, via, hashtag, id_proyecto, actualizacion) {
    //console.log("PopUp linkedin");
    social_counter(id_proyecto, "twitter", actualizacion);

    var lkurl = host + request_path;
    var lktitle = nombre_proyecto;
    var lksummary = descripcion_proyecto;
    var lkhost = host;
    var via = via;
    var hashtag = hashtag;
    var sharerURL = "https://twitter.com/share?url=" + encodeURI(lkurl) + "&via=" + encodeURI(via) + "&title=" + encodeURI(lktitle) + "&related=somosRENKA" + "&hashtags=" + encodeURI(hashtag) + "&text=" + encodeURI(lksummary);
    //console.log(sharerURL);
    window.open(
        sharerURL,
        'linkedin-share-dialog',
        'width=626,height=436');
    return false;
}


    function share_fb(host, url, titulo, descripcion, url_img, id_proyecto, actualizacion)
    {
        social_counter(id_proyecto, "facebook", actualizacion);
        FB.ui(
                {
                    method: 'feed',
                    name: titulo,
                    link: host + url,
                    picture: host +'/' +url_img,
                    caption: 'Impulsando negocios | RENKA',
                    description: descripcion,
                    message: 'PLOP'
                }
        );
    }



// Funcion para Compartir
function compartir(host, link, nombre_proyecto, descripcion_proyecto, imagen) {
    console.log(host);
    console.log(link);
    console.log(autoscape(nombre_proyecto));
    console.log(autoscape(descripcion_proyecto));
    console.log(imagen);

    FB.ui(
        {
            method: 'feed',
            name: nombre_proyecto,
            link: host + link,
            picture: host + '/'+imagen,
            caption: 'www.Somosrenka.com Invierte y Apoya Proyectos',
            description: descripcion_proyecto,
            message: "Apoyemos el proyecto " + nombre_proyecto
        },
        function (response) {
            if (response && response.post_id) {
                //alert('Post Publicado.');
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


function compartir_proyecto(host, path, titulo_proyecto, imagen_url, descripcion_proyecto) {
    FB.api(
        'me/objects/renka_oficial:proyecto',
        'post',
        {
            'og:url': 'http://samples.ogp.me/552059264932836',
            'og:title': 'Sample Proyecto',
            'og:type': 'renka_oficial:proyecto',
            'og:image': 'https://fbstatic-a.akamaihd.net/images/devsite/attachment_blank.png',
            'og:description': '',
            'fb:app_id': '545359655602797'
        },
        function (response) {
            console.log(response);
            // handle the response
        }
    );
}


function compartir_proyecto(host, path, titulo_proyecto, imagen_url, descripcion_proyecto) {
    FB.api(
        'me/objects/renka_oficial:proyecto',
        'post',
        {
            'og:url': 'http://samples.ogp.me/552059264932836',
            'og:title': 'Sample Proyecto',
            'og:type': 'renka_oficial:proyecto',
            'og:image': 'https://fbstatic-a.akamaihd.net/images/devsite/attachment_blank.png',
            'og:description': '',
            'fb:app_id': '545359655602797'
        },
        function (response) {
            console.log(response);
            // handle the response
        }
    );
}

function compartir_proyecto_1(host, path) {
    FB.api(
        'me/renka_oficial:compartir',
        'post',
        {
            'proyecto': host + path
        },
        function (response) {
            // handle the response
        }
    );
}


function og_proyecto(host, path) {
    FB.ui({
        method: 'share_open_graph',
        action_type: 'me/renka_oficial:compartir',

        action_properties: JSON.stringify({
            proyecto: host + path
        })
    }, function (response) {
        console.log(response);
    });
    // action_type: 'matchadviceuk:share',    // appNameSpace:myCustomAction

}

function social_counter(id_proyecto, red_social, actualizacion) {
    console.log("social counter, id_proyecto = "+id_proyecto)
    $.ajax({
        data: {"id_p": id_proyecto, "r": red_social, "a": actualizacion},
        type: "post",
        url: "/estadisticas/ajax_social_counter/",
        success: function () {
            console.log("exito al conectarse");
        },
        error: function (xhr, errmsg, err) {
            console.log("error al conecta");
        }
    });
}

        function compartir_cupon(host, path)
        {
            console.log("compartir_cupon");
            FB.api(
                'me/renka_oficial:compartir',
                'post',
                {
                    'proyecto': host+path
                },
                function (response) {
                    // handle the response
                }
            );
        }

        function compartir_cp(host, path, titulo_proyecto, imagen_url, descripcion_proyecto)
        {
            FB.api(
                'me/objects/renka_oficial:proyecto',
                'post',
                {
                    'og:url': 'http://samples.ogp.me/552059264932836',
                    'og:title': 'Sample Proyecto',
                    'og:type': 'renka_oficial:proyecto',
                    'og:image': 'https://fbstatic-a.akamaihd.net/images/devsite/attachment_blank.png',
                    'og:description': '',
                    'fb:app_id': '545359655602797'
                },
                function (response) {
                    console.log(response);
                    // handle the response
                }
            );
        }

            function stream_cupon(host) {
        FB.ui({
                    method: 'stream.share',
                    u: host+'/media/usuarios/122/282aa010-9555-4874-9ef3-df6efa2f7308.jpg'
                },
                function (response) {
                    alert(response);
                }
        );
    };

