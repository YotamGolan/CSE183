

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
        pixel_count: 0,
        colorWell: null,
        color: "#0000ff",
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    


    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        
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

        var imgObj = new Image();
       
        axios.get(load_users_image_url).then(function (response) {
            imgObj.src = response.data.image;
        });

        console.log(imgObj.src);
        imgObj.onload = function() {
            app.vue.canvas.drawImage(imgObj, 0, 0);
        }

    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);

