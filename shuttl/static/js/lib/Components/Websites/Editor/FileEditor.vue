<template>
    <div id="editor" name="content"><slot></slot></div>
</template>

<script>

export default {
    props: ['filetype', 'fileid'],
    data: function () {
        return {
            filename: '',
            parent_dir: window.current_dir,
            content: '',
            dirs: []
        }
    },
    ready: function() {
        if (this.filetype != 'image') {
          this.editor = ace.edit("editor");
          this.editor.setTheme("ace/theme/monokai");
          this.editor.fileid = this.fileid;
          this.editor.filetype = this.filetype || "generic";
          var ext = this.filetype;
          var mode = "ace/mode/plain_text";
          switch(ext) {
              case "html":
                  mode = "ace/mode/twig";
                  break;
              case "css":
                  mode = "ace/mode/css";
                  break;
              case "js":
                  mode = "ace/mode/javascript";
                  break;
              case "twig":
                  mode = "ace/mode/twig";
                  break;
              default:
                  break;
          }
          this.editor.getSession().setMode(mode);
          window.editor = this.editor;
        }
    }
}
</script>

<style lang="sass" scoped>
    #editor {
        width: 100%;
        height: 100vh;
    }
    #filecreate {
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
