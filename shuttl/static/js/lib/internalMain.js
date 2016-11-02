window.globals = [];

var event = new Event('save');

document.saveAction = function() {
   parent.document.dispatchEvent(event);
}

import Vue from 'vue';
import VueResource from "vue-resource";
import String from "./String.js";
import Save from "./SaveHandler.js";
import Wysiwyg from "./Components/InternalComponents/Wysiwyg.vue"
import Text from "./Components/InternalComponents/Text.vue"
import Obtain from "./Components/InternalComponents/Obtain.vue"
import saveLevel from "./SaveLevel.js";
import MultiItem from "./Components/InternalComponents/MultiContent.vue"
import Multiblock from "./Components/InternalComponents/MultiBlock.vue";

Vue.component("shuttl-wysiwyg", Wysiwyg);
Vue.component("shuttl-text", Text);
Vue.component("shuttl-obtain", Obtain);
Vue.component("shuttl-multiitem", MultiItem);
Vue.component("shuttl-multiblock", Multiblock)

Vue.config.delimiters = ['${', '}'];

Vue.use(VueResource);

window.vm = new Vue({
    el: "body"
});

window.save = function() {
    console.log( vm.$root.$children);
    var content = {};
    content["local"] = saveLevel(window.vm.$root);
    content["global"] = {};
    for (var i = 0; i < window.globals.length; i++) {
        var globalObj = window.globals[i];
        content["global"][globalObj.self_id] = globalObj.getAllData();
    }
    return content;
}

import Tour from "./Tour.js"


window.startTour = function() {
    Tour.start(true);
}
