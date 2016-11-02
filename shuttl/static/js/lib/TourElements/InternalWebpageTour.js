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
            title: 'Edit content',
            text: 'The webpage is edited directly inline.<br/>When you hover over an editable section,<br/>you\'ll see a border',
            attachTo: '.editiable bottom',
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
                action: tour.next
            }
        ]
        });

        tour.addStep('step2', {
            title: 'Edit content',
            text: 'The webpage is edited directly inline.<br/>When you hover over an editable section,<br/>you\'ll see a border',
            attachTo: '.editiable bottom',
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
                action: tour.next
            }
        ]
        });

        tour.addStep('step3', {
            title: 'Edit content',
            text: 'For example, this is a what you see is what you get (or "wysiwyg") block.',
            attachTo: '.editiable bottom',
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
                action: function () {
                    tour.cancel();
                    parent.ResumeTour();
                }
            }
        ]
        });

        return tour;
    }
}