/**
 * Created by Jankrloz on 01/05/2015.
 */


$("#form").steps({
    bodyTag: "fieldset",
    enableCancelButton: false,
    showFinishButtonAlways: false,
    transitionEffect: 'fade',
    enableAllSteps: false,
    suppressPaginationOnFocus: true,
    saveState: true,
    autoFocus: true,
    transitionEffectSpeed: 100,
    titleTemplate: '<span class="step-title"><span class="number">#index#.</span> #title#</span>',

    labels: {
        cancel: "Cancelar",
        finish: "Finalizar",
        next: "Siguiente <i class='fa fa-chevron-right'></i>",
        previous: "<i class='fa fa-chevron-left'></i> Anterior",
        loading: "Cargando ..."
    },

    onStepChanging: function (event, currentIndex, newIndex)
    {

        // Always allow going backward even if the current step contains invalid fields!
        var form;
        if (currentIndex > newIndex) {
            return true;
        }
        else {
            $('.wizard-error p').html('');
        }


        form = $(this);

        /*
        // Clean up if user went backward before
        if (currentIndex < newIndex)
        {
            // To remove error styles
            $(".body:eq(" + newIndex + ") label.error", form).remove();
            $(".body:eq(" + newIndex + ") .error", form).removeClass("error");
        }
         */

        // Disable validation on fields that are disabled or hidden.
        //form.validate().settings.ignore = ":disabled,:hidden";

        // Start validation; Prevent going forward if false
        return form.valid();
    },
    onStepChanged: function (event, currentIndex) {

        var pasos = 6;
        if ($('.tipo_proyecto').html() == 'Recompensas') {
            pasos = 5;
        }
        if (currentIndex >= pasos - 1) {
            $('a[href="#finish"]').closest('li').show();
        }
        else {
            $('a[href="#finish"]').closest('li').hide();
        }
    },
    onFinishing: function (event, currentIndex)
    {
        var form = $(this);

        // Disable validation on fields that are disabled.
        // At this point it's recommended to do an overall check (mean ignoring only disabled fields)
        //form.validate().settings.ignore = ":disabled";

        // Start validation; Prevent form submission if false
        return form.valid();
    },
    onFinished: function (event, currentIndex)
    {
        var form = $(this);

        // Submit form input
        form.submit();
    }
}).validate({
    errorPlacement: function (error, element)
    {
        $('div.validate-error.' + $(element).attr('data-error')).html(error);
        $('.wizard-error p').html('* Hubo algunos errores');
    },
});