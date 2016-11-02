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
            title: 'Save Button',
            text: 'This button Saves the file. You can also use "ctrl-s" or "cmd-s" (on mac).',
            attachTo: '#save_btn bottom',
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
            title: 'Publish Button',
            text: 'This button publishes the files. \nAfter you press this button, \nyour changes will be sent to you server and  that whole world will see them!',
            attachTo: '#save_btn bottom',
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
            title: 'That\'s all',
            text: 'That is all on this page, try clicking on another page!',
            buttons: [
            {
                text: 'Ok',
                classes: 'shepherd-button-example-primary',
                action: cancel("webpageComplete", tour)
            }
        ]
        });

        return tour;
    }
}