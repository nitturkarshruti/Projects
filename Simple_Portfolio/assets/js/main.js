/*
    Dopetrope by HTML5 UP
    html5up.net | @ajlkn
    Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

    var $window = $(window),
        $body = $('body');

    // Breakpoints.
    breakpoints({
        xlarge: [ '1281px', '1680px' ],
        large: [ '981px', '1280px' ],
        medium: [ '737px', '980px' ],
        small: [ null, '736px' ]
    });

    // Play initial animations on page load.
    $window.on('load', function() {
        window.setTimeout(function() {
            $body.removeClass('is-preload');
        }, 100);
    });

    // Dropdowns.
    $('#nav > ul').dropotron({
        mode: 'fade',
        noOpenerFade: true,
        alignment: 'center'
    });

    // Nav.

    // Title Bar.
    $('<div id="titleBar">' +
        '<a href="#navPanel" class="toggle"></a>' +
        '</div>')
    .appendTo($body);

    // Panel.
    $('<div id="navPanel">' +
        '<nav>' +
        $('#nav').navList() +
        '</nav>' +
        '</div>')
    .appendTo($body)
    .panel({
        delay: 500,
        hideOnClick: true,
        hideOnSwipe: true,
        resetScroll: true,
        resetForms: true,
        side: 'left',
        target: $body,
        visibleClass: 'navPanel-visible'
    });

    // ==========================
    // Text Changing Functionality
    // ==========================

    // Define the text elements and initialize variables
    var texts = ["PHP Developer", "Java Full Stack Developer"];
    var index = 0;
    var $textElement = $('#dynamicText'); // Ensure the HTML element has id="dynamicText"

    // Function to change text every 3 seconds
    function changeText() {
        if ($textElement.length > 0) { // Ensure the element exists
            $textElement.fadeOut(500, function() {
                $(this).text(texts[index]).fadeIn(500);
                index = (index + 1) % texts.length;
            });
        }
    }

    // Set interval for changing text
    setInterval(changeText, 3000);

})(jQuery);
