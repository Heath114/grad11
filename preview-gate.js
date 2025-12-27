(function() {
    'use strict';
    
    // Check if preview access is granted
    if (!localStorage.getItem('preview_access')) {
        window.location.replace('preview.html');
    }
})();
