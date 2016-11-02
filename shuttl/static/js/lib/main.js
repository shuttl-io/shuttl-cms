/**
 * Created by Yoseph on 6/16/16.
 */


var baseURL = "shuttl.com:5000";
var doc = document;

doc.saveAction = function() {
    if (doc.getElementById("save_btn")){
        doc.getElementById("save_btn").click();
        return;
    }
    var event = new Event('save');
    parent.document.dispatchEvent(event);
}

import Vue from 'vue';
import VueResource from "vue-resource";
import String from "./String.js";
import Save from "./SaveHandler.js";
import Organizations from "./Components/Organization/Organizations.vue"
import Websites from "./Components/Websites/Websites.vue"
import InternalNav from "./Components/NavCompenents/InternalNav.vue"
import WebpageForm from "./Components/Websites/Webpages/WebpageForm.vue"
import FileEditor from "./Components/Websites/Editor/FileEditor.vue"

Vue.use(VueResource);

Vue.component("shuttl-organizations", Organizations);
Vue.component("shuttl-websites", Websites);
Vue.component("shuttl-internalnav", InternalNav);
Vue.component("shuttl-newwebpage", WebpageForm);
Vue.component("shuttl-editfile", FileEditor);

Vue.config.delimiters = ['${', '}'];

window.vm = new Vue({
    el: "body"
});

$("#websiteObjects").change(function(e){
	window.location = $("#websiteObjects").val();
});
doc.addEventListener('save', function (e) {
    doc.saveAction();
}, false);

import Tour from "./Tour.js"

Tour.start();

window.ResumeTour = function () {
    Tour.resumeInternal();
}
