

let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        canvas: null,
        objCanvas: null,
        w: 0,
        h: 0,
        x: 0,
        y: 0,
        clr: 'black',
        lineWidth: 2,
        drawState: false,
        counter: 0,
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.drawline = function(e) {
        if(app.vue.drawState) {
            app.draw(app.vue.x, app.vue.y, e.offsetX, e.offsetY);
            app.vue.x = e.offsetX;
            app.vue.y = e.offsetY;
        }
    }

    app.draw = function (x1, y1, x2, y2) {
        let ctx = app.vue.canvas;
        ctx.beginPath();
        ctx.lineWidth = app.vue.lineWidth;
        ctx.strokeStyle = app.vue.clr;
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        axios.post
        ctx.stroke();
        ctx.closePath();
        // add set interval for loading new drawing
    }

    app.setGreen = function() {
        app.vue.clr = "green";
    }
    app.setWhite = function() {
        app.vue.clr = "white";
    }
    app.setYellow = function() {
        app.vue.clr = "yellow";
    }
    app.setOrange = function() {
        app.vue.clr = "orange";
    }
    app.setBlack = function() {
        app.vue.clr = "black";
    }
    app.setBlue = function() {
        app.vue.clr = "blue";
    }
    app.setRed = function() {
        app.vue.clr = "red";
    }
    app.incrWidth = function() {
        if(app.vue.lineWidth <= 13) {
            app.vue.lineWidth = app.vue.lineWidth + 1;
        }
    }
    app.decrWidth = function() {
        if(app.vue.lineWidth >= 3) {
            app.vue.lineWidth = app.vue.lineWidth - 1;
        }
    }

    app.clear = function() {
        var m = confirm("Want to clear");
        if (m) {
            app.vue.canvas.clearRect(0, 0, app.vue.w, app.vue.h);
            document.getElementById("canvasimg").style.display = "none";
        }
    }

    app.startDrawing = function(e) {
        app.vue.x = e.offsetX;
        app.vue.y = e.offsetY;
        app.vue.drawState = true;
    }

    app.save = function() {
        //document.getElementById("canvasimg").style.border = "2px solid";
        var dataURL = app.vue.objCanvas.toDataURL();
        //document.getElementById("canvasimg").src = dataURL;
        //document.getElementById("canvasimg").style.display = "inline";
    }

    app.stopDrawing = function(e) {
      if (app.vue.drawState) {
        app.drawline(e);
        app.vue.x = 0;
        app.vue.y = 0;
        app.vue.drawState = false;
      }
    }
    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        drawline: app.drawline,
        draw: app.draw,
        startDrawing: app.startDrawing,
        stopDrawing: app.stopDrawing,
        setGreen: app.setGreen,
        setWhite: app.setWhite,
        setOrange: app.setOrange,
        setYellow: app.setYellow,
        setBlack: app.setBlack,
        setRed: app.setRed,
        setBlue: app.setBlue,
        incrWidth: app.incrWidth,
        decrWidth: app.decrWidth,
        clear: app.clear,
        save: app.save,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        var c = document.getElementById("myCanvas");
        app.vue.objCanvas = c;
        app.vue.w = c.width;
        app.vue.h = c.height;
        //axios.get() get data url
        app.vue.canvas = c.getContext('2d'); // link up recent data url here

    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

