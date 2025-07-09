(function($) {
    // Initialize dashboard when document is ready
    $(document).ready(function() {
        initDashboard();
    });
    
    function initDashboard() {
        // Add animation to stat cards
        animateStatCards();
        
        // Add refresh button
        addRefreshButton();
        
        // Add date range selector
        addDateRangeSelector();
    }
    
    function animateStatCards() {
        $('.stat-card').each(function(index) {
            var $card = $(this);
            setTimeout(function() {
                $card.addClass('animated fadeInUp');
            }, index * 100);
            
            // Animate numbers
            var $number = $card.find('.number');
            var finalValue = parseInt($number.text(), 10);
            
            if (!isNaN(finalValue)) {
                $number.text('0');
                $({ value: 0 }).animate({ value: finalValue }, {
                    duration: 1000,
                    easing: 'swing',
                    step: function() {
                        $number.text(Math.floor(this.value));
                    },
                    complete: function() {
                        $number.text(finalValue);
                    }
                });
            }
        });
    }
    
    function addRefreshButton() {
        var $refreshButton = $('<button>')
            .addClass('button')
            .text('Refresh Data')
            .css({
                'position': 'absolute',
                'top': '20px',
                'right': '20px'
            })
            .click(function() {
                location.reload();
            });
        
        $('.dashboard-container h1').css('position', 'relative').append($refreshButton);
    }
    
    function addDateRangeSelector() {
        // This is a placeholder for future date range selector implementation
        // Would require additional backend support to filter by date range
        console.log('Date range selector would be implemented here');
    }
})(django.jQuery); 