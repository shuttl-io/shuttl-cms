import Dashboard from "./TourElements/DashboardTour.js";
import Show from "./TourElements/ShowTour.js";
import Webpage from "./TourElements/WebpageTour.js"
import InternalTour from "./TourElements/InternalWebpageTour.js"
import Tour from "./TourElements/WebpagePt2Tour.js"

function GetTourForPage(url, internal) {
    var tour = null;
    var reWebsite = /(\/show\/[0-9]\/)/;
    var reWebpage = /(\/show\/[0-9]+\/[0-9]+\/)/;

    if (url === "/home") {
        if (!localStorage.dashComplete)
            tour = Dashboard;
    }
    else if (reWebpage.exec(url)) {
        if (!localStorage.webpageComplete)
            tour = Webpage;
    }
    else if (reWebsite.exec(url)) {
        if (!localStorage.websiteComplete)
            tour = Show;
    }
    else if (internal) {
        tour = InternalTour;
    }
    if (tour != null)
        return tour.tour();
    return null
}

export default {
    start: function (internal) {
        var internal = internal || false;
        var tour = GetTourForPage(window.location.pathname, internal);
        if(tour)
            tour.start()
    },
    resumeInternal: function() {
        var tour = Tour.tour();
        tour.start()
    }
}
