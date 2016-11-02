function cancel(command, tour) {
    return function() {
        localStorage[command] = true;
        tour.cancel();
    }
}

export default {
    tour: function() {
        var tour = new Shepherd.Tour({
            defaults: {
                classes: 'shepherd-theme-arrows absTop',
            }
        });

        tour.addStep('step1', {
            text: 'This part of the tour will take you through content entry interface!',
            title: 'Welcome Back!',
            classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
            buttons: [
                {
                    text: 'No Thanks',
                    classes: 'shepherd-button-secondary',
                    action: cancel("webpageComplete", tour)
                },
                {
                    text: "Let's go!",
                    classes: 'shepherd-button-example-primary',
                    action: function() {
                        $(".cellContainer .cell.map a").css("z-index", "0");
                        $(" header.internal").css("z-index", "0");
                        tour.next();
                    }
                }
            ]
        });

        tour.addStep('step2', {
            title: 'Highlighted files',
            text: 'The file that is highlighted is the current page',
            attachTo: '.highlighted right',
            buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("webpageComplete", tour)
            },
            {
                text: 'Back',
                classes: 'shepherd-button-secondary',
                action: tour.back
            },
            {
                text: 'Continue',
                classes: 'shepherd-button-example-primary',
                action: function() {
                    document.getElementById('mainRender').contentWindow.startTour();
                    tour.cancel();
                }
            }
        ]
        });

        return tour;
    }
}