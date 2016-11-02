function cancel(command, tour) {
    return function() {
        localStorage[command] = true;
        tour.cancel();
    }
}

function showTour() {
    var tour = new Shepherd.Tour({
        defaults: {
            classes: 'shepherd-theme-arrows absTop',
        }
    });

    tour.addStep('step1', {
        text: 'This part of the tour will take you through the Website dashboard!',
        title: 'Welcome Back!',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'No',
                classes: 'shepherd-button-secondary',
                action: cancel("websiteComplete", tour)
            },
            {
                text: 'Yes',
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
        title: 'Website shortcut',
        text: 'This this is a shortcut to all your websites and dashboard!',
        attachTo: '#websiteObjects bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: function() {
                    $(".cellContainer .cell.map a").css("z-index", "1000");
                    $(" header.internal").css("z-index", "10");
                    cancel("websiteComplete", tour)();
                }
            },
            {
                text: 'Back',
                classes: 'shepherd-button-secondary',
                action: function() {
                    $(".cellContainer .cell.map a").css("z-index", "1000");
                    $(" header.internal").css("z-index", "10");
                    tour.back();
                }
            },
            {
                text: 'Continue',
                classes: 'shepherd-button-example-primary',
                action: function() {
                    $(".cellContainer .cell.map a").css("z-index", "1000");
                    $(" header.internal").css("z-index", "10");
                    tour.next();
                }
            }
        ]
    });

    tour.addStep('step3', {
        title: 'New Menu',
        text: 'This is the New menu. <br/>You can make new directories, css <br/>or javascript files, <br/>templates and webpages.',
        attachTo: '#new-btn bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("websiteComplete", tour)
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
                    // $("#new-btn").trigger("click");
                    window.vm.$children[0].show =true;
                    setTimeout(function() {
                        tour.next();
                    }, 1);
                    // tour.next();
                }
            }
        ]
    });

    tour.addStep('step4', {
        title: 'New Menu',
        text: 'These are webpages that are made by templates.<br/>These are the objects that get made into static webpages',
        attachTo: '.webpageTypes.submenu-items left',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("websiteComplete", tour)
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
        title: 'New Menu',
        text: 'You can also make files (Template files, css files, <br/>javascript files, images, etc) or a new Directory',
        attachTo: '.fileTypes.submenu-items left',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("websiteComplete", tour)
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
                    // $("#new-btn").trigger("click");
                    window.vm.$children[0].show = false;
                    setTimeout(function() {
                        tour.next();
                    }, 1);
                    // tour.next();
                }
            }
        ]
    });

    tour.addStep('step6', {
        title: 'File Tree',
        text: 'This shows all of the files, templates, directories, <br/>and webpages associated with this website.',
        attachTo: '.cell.map right',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("websiteComplete", tour)
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
                    // $("#new-btn").trigger("click");
                    window.vm.$children[0].show = false;
                    setTimeout(function() {
                        tour.next();
                    }, 1);
                    $(".cellContainer .cell.map a").css("z-index", "0");
                    $(" header.internal").css("z-index", "0");
                }
            }
        ]
    });

    tour.addStep('step7', {
        title: 'File Tree',
        text: 'This is the root Directory.<br/>Everything else exsists inside of this directory.',
        attachTo: '.dir.root bottom',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: function() {
                    $(".cellContainer .cell.map a").css("z-index", "1000");
                    $(" header.internal").css("z-index", "10");
                    cancel("websiteComplete", tour)();
                }
            },
            {
                text: 'Back',
                classes: 'shepherd-button-secondary',
                action: function() {
                    $(".cellContainer .cell.map a").css("z-index", "1000");
                    $(" header.internal").css("z-index", "10");
                    tour.back();
                }
            },
            {
                text: 'Continue',
                classes: 'shepherd-button-example-primary',
                action: function () {
                    // $("#new-btn").trigger("click");
                    window.vm.$children[0].show = false;
                    setTimeout(function() {
                        tour.next();
                    }, 1);
                    $(".cellContainer .cell.map a").css("z-index", "1000");
                    $(" header.internal").css("z-index", "10");
                }
            }
        ]
    });

     tour.addStep('step8', {
        title: 'Next Steps',
        text: 'This is all we have to show you on the website dashboard.<br/>To continue, make a new file, webpage, or click on a file.',
        classes: 'shepherd shepherd-open shepherd-theme-arrows shepherd-transparent-text',
        buttons: [
            {
                text: 'stop',
                classes: 'shepherd-button-secondary',
                action: cancel("websiteComplete", tour)
            },
            {
                text: 'Back',
                classes: 'shepherd-button-secondary',
                action: tour.back
            },
            {
                text: 'Finish',
                classes: 'shepherd-button-example-primary',
                action: function () {
                    tour.next();
                }
            }
        ]
    });

    return tour;
}

export default {
    tour: showTour
}