<template>
    <form id="filecreate">
        <div id="newEditor" name="content"></div>
        <center>
            <label for="name" class="sr-only">File Name</label>
            <p>
                <input type="test" name="name" placeholder="File Name" required v-model="filename" v-on:change="changeExt">
                <label for="parent" class="sr-only">Parent Directory</label>

                <select name="parent_id" v-model="parent_dir" id="parent">
                    <option v-for="dir in dirs" v-bind:value="dir.id" id="dir-${dir.id}"> ${dir.fullPath} </option>
                </select>
            </p>



            <label for="file" class="sr-only">File</label>
            <p>
                <input type="file" name="file" accept="*/*" v-model="file" id="file-select">
            </p>
        </center>
        <p>
            <center><button v-on:click.prevent="submit">Create File</button></center>
        </p>
    </form>
</template>

<script>

export default {
    data: function () {
        return {
            filename: "",
            parent_dir: window.current_dir,
            content: "",
            dirs: []
        }
    },
    ready: function() {
        this.editor = ace.edit("newEditor");
        this.editor.setTheme("ace/theme/monokai");
        this.editor.getSession().setMode("ace/mode/plain_text");
        this.$http.get("/website/{0}/files/dir/".format(window.website_id)).then((response) => {
            if (response.status == 200) {
                this.dirs = response.data;

                $("#parent").val(window.current_dir);
            }
            else {
                console.log("An error occured. Code: {0}".format(response.status));
            }
        }, (response) => {
            console.log("An error occured. Code: {0}".format(response.status));
        });
    },
    methods: {
        changeExt: function() {
            var ext = this.filename.split(".");
            if (ext.length < 2){
                 this.editor.getSession().setMode("ace/mode/plain_text");
                 return;
            }
            var mode = "ace/mode/plain_text";
            switch(ext[ext.length - 1]) {
                case "html":
                    mode = "ace/mode/twig";
                    break;
                case "css":
                    mode = "ace/mode/css";
                    break;
                case "js":
                    mode = "ace/mode/javascript";
                    break;
                default:
                    break;
            }
            this.editor.getSession().setMode(mode);
        },
        submit: function() {
            var file_parts =  this.filename.split(".");
            var ndx = file_parts.length - 1;
            var ext = file_parts[ndx];
            var formData = new FormData();
            formData.append("parent_id", this.parent_dir);
            formData.append("name", file_parts.join("."));
            if (this.editor.getValue() != "") {;
                formData.append("file_contents", this.editor.getValue());
            }
            else if (this.file) {
                var file = document.getElementById('file-select').files[0];
                formData.append("file",  file, file.name);
            }

            this.$http.post("/website/{0}/files/{1}/".format(window.website_id, ext), formData).then((response) => {
                    window.location = "/show/{0}/{1}".format(window.website_id, response.data.id);
            }, (response) => {
                switch (response.response.status){
                    case 404:
                        alert("File not found");
                        break;

                     case 409:
                        alert("A file with that name already exists. Choose a new name and try again.");
                        break;

                    default:
                        alert("Something went wrong =(\n If this keeps happening, please contact us at help@shuttl.io");
                        break;
                }
                console.log("An error Occured: {0}".format(response.status));
            });
        }
    }
}
</script>

<style lang="sass" scoped>
    #newEditor {
        width: 100%;
        height: 80%;
    }
    #filecreate {
      height: 100%;
        .centered {
            text-align: center;
        }
        button {
            width: 100px;
            padding: 10px 0;
            margin: 0 auto;
        }
    }
</style>
