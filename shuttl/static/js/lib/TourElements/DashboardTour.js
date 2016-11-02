function cancel(command, tour) {
    return function() {
        localStorage[command] = true;
        tour.cancel();
    }
}

function dashboard() {
    var tour = new Shepherd.Tour({
        defaults: {
            classes: 'shepherd-theme-arrows',
        }
    });

    tour.addStep('step1', {
        text: "Why don't you take a tour of shuttl?",
        title: 'Welcome to the shuttl Demo!',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'No',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
            },
            {
                text: 'Yes',
                classes: 'shepherd-button-example-primary',
                action: tour.next
            }
        ]
    });

    tour.addStep('step2', {
        title: 'Organization dashboard',
        text: 'This is where you see your websites. <br/>We built Shuttl so that you can maintain multiple websites without a seperate account.',
        attachTo: '.main-content bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
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

    var step3 =  'This is how you create a website.'
    step3 += '<br/>We believe that everything should be as simple as possible. <br/>Simply enter the name of the website and press add.';
    tour.addStep('step3', {
        title: 'Website Creation',
        text: step3,
        attachTo: '.inputForm bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
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

    tour.addStep('step4', {
        title: 'Website List',
        text: "This section lists out the websites that belong to your organization.",
        attachTo: '.websites top',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
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

    tour.addStep('step5', {
        title: 'Website Name',
        text: "This is the name of your website and it links to the website dashboard",
        attachTo: '.cell.input a bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
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

    tour.addStep('step6', {
        title: 'Rename',
        text: "Click this button to rename your website",
        attachTo: '.cell.edit bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
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

    tour.addStep('step7', {
        title: 'Delete',
        text: "Click this button to delete your website",
        attachTo: '.cell.delete bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
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

    tour.addStep('step8', {
        title: 'Delete Multiple',
        text: "Check this checkbox to be able to delete multiple websites at once",
        attachTo: '.cell.check bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
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
                    $(".cell.check input").trigger("click");
                    setTimeout(function(){
                        tour.next();
                    }, 5);
                    
                }
            }
        ]
    });

     tour.addStep('step8', {
        title: 'Delete Multiple',
        text: "Once all sites are checked, use this to delete them.",
        attachTo: '#delete bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
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
                    $(".cell.check input").trigger("click");
                    tour.next();
                }
            }
        ]
    });

    tour.addStep('step9', {
        title: 'Moving On',
        text: "This is it for this this portion of the tour. Click on a website to continue the tour.",
        attachTo: '#main-nav bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("dashComplete", tour)
            },
            {
                text: 'Back',
                classes: 'shepherd-button-secondary',
                action: tour.back
            },
            {
                text: 'Finish',
                classes: 'shepherd-button-example-primary',
                action: cancel("dashComplete", tour)
            }
        ]
    });
    return tour; 
}

export default {
    tour: dashboard
}