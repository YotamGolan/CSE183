

let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        c: null,
        canvas: null,
        //canvasOffset: $("#canvas").offset(),
        //offsetX: canvasOffset.left,
        //offsetY: canvasOffset.top,
        r: 255,
        g: 0,
        b: 0,
        x: 0,
        y: 0,
        w: 0,
        h: 0,
        colorWell: null,
        color: "#0000ff",
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.setPixel = function (x, y, red, green, blue) {
            pixPos = ((~~x) + (~~y)) * 4;
            var pxData = app.vue.canvas.getImageData(x, y, 1, 1);
            pxData.data[0] = app.vue.r;
            pxData.data[1] = app.vue.g;
            pxData.data[2] = app.vue.b;
            pxData.data[3] = 255;
            app.vue.canvas.putImageData(pxData, x, y);
    }

    app.handleMouseDown = function (e) {
            var imgObj = new Image();
            mouseX = e.offsetX;
            mouseY = e.offsetY;
            console.log(mouseX, mouseY, app.vue.r, app.vue.g, app.vue.b);
            // Put your mousedown stuff here
            app.setPixel(mouseX, mouseY, app.vue.r, app.vue.g, app.vue.b);
            axios.post(set_pixel_url, {
                x: mouseX,
                y: mouseY,
                r: app.vue.r,
                g: app.vue.g,
                b: app.vue.b,
            }).then(function (response){
                imgObj.src = response.data.image;
                imgObj.onload = function() {
                    app.vue.canvas.drawImage(imgObj, 0, 0);
                }
            });// Add image load here
    }

    app.watchColorPicker = function (event) {
        document.querySelectorAll("canvas").forEach(function(p) {
            p.style.color = event.target.value;
        });
    }

    app.startup = function () {
        app.vue.colorWell = document.querySelector("#colorWell");
        app.vue.colorWell.value = app.vue.color;
        app.vue.colorWell.addEventListener("input", app.updateFirst, false);
        app.vue.colorWell.addEventListener("change", app.updateAll, false);
        app.vue.colorWell.select();
    }

    app.updateFirst = function (event) {
        var p = document.querySelector("canvas");

        if (p) {
            p.style.color = event.target.value;
            console.log(p.style.color);
        }
    }

    app.updateAll = function (event) {
        document.querySelectorAll("canvas").forEach(function(p) {
            p.style.color = event.target.value;
            var count = 4;
            app.vue.r = app.vue.g = app.vue.b = 0;
            while(p.style.color[count] != ',') {
                app.vue.r += p.style.color[count];
                console.log(count);
                count++;
            }
            console.log(count);
            count += 2;
            while(p.style.color[count] != ',') {
                app.vue.g += p.style.color[count];
                count++;
            }
            count += 2;
            while(p.style.color[count] != ')') {
                app.vue.b += p.style.color[count];
                count++;
            }
            app.vue.r = parseInt(app.vue.r, 10);
            app.vue.g = parseInt(app.vue.g, 10);
            app.vue.b = parseInt(app.vue.b, 10);
            console.log(app.vue.r, app.vue.g, app.vue.b);
        });
    }


    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        setPixel: app.setPixel,
        handleMouseDown: app.handleMouseDown,
        watchColorPicker: app.watchColorPicker,
        startup: app.startup,
        updateAll: app.updateAll,
        updateFirst: app.updateFirst,
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
        app.vue.c = document.getElementById("myCanvas");
        app.vue.canvas = app.vue.c.getContext('2d'); // link up recent data url here
        app.vue.w = app.vue.c.width;
        app.vue.h = app.vue.c.height;

        //var imgPath = 'images/download.png';
        var imgObj = new Image();
        /*imgObj.src = imgPath;
        imgObj.onload = function() {
            app.vue.canvas.drawImage(imgObj, 0, 0);
        }*/
        axios.get(load_image_url).then(function (response) {
            imgObj.src = response.data.image;
        });

        console.log(imgObj.src);
        imgObj.onload = function() {
            app.vue.canvas.drawImage(imgObj, 0, 0);
        }
        app.startup();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

