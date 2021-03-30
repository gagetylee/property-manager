animate_toggle = function() {
  $('#content').slideToggle()
}

setup = function() {
    $('#options').click(animate_toggle)
}

jQuery(document).ready(setup)
