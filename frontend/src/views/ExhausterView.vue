<template>
<!-- <v-container style="height: 90vh;"> -->
<v-row
    class="mb-6"
    style="width:80%;"
    no-gutters
>
    <v-col
        cols="12"
        sm="12"
        md="12"
        class="ps-2"
        no-gutters
    >
        <!-- <v-img id="svgimage"
            src="exhauster.svg"
        >
        </v-img> -->

        <object
            @load="onSvgLoaded"
            id="svgobject"
            data="exhauster.svg"
            type="image/svg+xml"
        ></object>

        <!-- <svg
            
        ></svg> -->

    </v-col>
</v-row>
    <!-- <v-progress-linear
        :v-model="50"
        height="25"
        x="100px"
        y="100px"
        >
        50%
    </v-progress-linear> -->
<!-- </v-container> -->
</template>

<script>
import { SVG, Text } from "@svgdotjs/svg.js"
export default {
    name: 'ExhausterView',

    data() {
        return {
            xxx : 0,
            sample_text_label : null,
            svgobject : null,
            data_model : {},
        }
    },

    methods: {
        onSvgLoaded(){
            console.log("onSvgLoaded():");
            this.svgobject = document.getElementById("svgobject").contentDocument;
            console.log("svg = ", this.svgobject);
            // this.sample_text_label = this.svgobject.getElementById('text787');
            // this.sample_text_label = $('#tspan785');
            // console.log("svg_text_label = ", this.sample_text_label);
            // this.sample_text_label.textContent = this.xxx;
        },

        updateSVG(){ // перерисовка SVG при получении очередной телеметрии
            // TODO переделать на табличную загрузку, слишком топорно

            var signal2label = [
                ["SM_Exgauster\\[3:43]","temperature1"         ],
                ["SM_Exgauster\\[3:14]","vibration_axial1"     ],
                ["SM_Exgauster\\[3:12]","vibration_horizontal1"],
                ["SM_Exgauster\\[3:13]","vibration_vertical1"  ],
                ["SM_Exgauster\\[3:44]","temperature2"         ],
                ["SM_Exgauster\\[3:17]","vibration_axial2"     ],
                ["SM_Exgauster\\[3:15]","vibration_horizontal2"],
                ["SM_Exgauster\\[3:16]","vibration_vertical2"  ],
                ["SM_Exgauster\\[3:45]","temperature3"         ],
                ["SM_Exgauster\\[3:47]","temperature4"         ],
                ["SM_Exgauster\\[3:48]","temperature5"         ],
                ["SM_Exgauster\\[3:49]","temperature6"         ],
                ["SM_Exgauster\\[3:50]","temperature7"         ],
                ["SM_Exgauster\\[3:20]","vibration_axial7"     ],
                ["SM_Exgauster\\[3:18]","vibration_horizontal7"],
                ["SM_Exgauster\\[3:19]","vibration_vertical7"  ],
                ["SM_Exgauster\\[3:51]","temperature8"         ],
                ["SM_Exgauster\\[3:23]","vibration_axial8"     ],
                ["SM_Exgauster\\[3:21]","vibration_horizontal8"],
                ["SM_Exgauster\\[3:22]","vibration_vertical8"  ],
                ["SM_Exgauster\\[3:52]","temperature9"         ],
                ["SM_Exgauster\\[3:60]","oil_temperature_after"   ],
                ["SM_Exgauster\\[3:59]","oil_temperature_before"  ],
                ["SM_Exgauster\\[3:54]","water_temperature_after" ],
                ["SM_Exgauster\\[3:53]","water_temperature_before"],
                ["SM_Exgauster\\[3:25]","temperature_before"   ],
                ["SM_Exgauster\\[3:62]","underpressure_before" ],
                ["SM_Exgauster\\[5:13]","gas_valve_position"   ],
                ["SM_Exgauster\\[5:9]" ,"rotor_current"   ],
                ["SM_Exgauster\\[5:11]","rotor_voltage"   ],
                ["SM_Exgauster\\[5:10]","stator_current"  ],
                ["SM_Exgauster\\[5:12]","stator_voltage"  ],
                ["SM_Exgauster\\[5:7]" ,"oil_level"       ],
                ["SM_Exgauster\\[5:8]" ,"oil_pressure"    ],
            ];

            console.log("this.data_model3 = ", this.data_model);
            for(var pair of signal2label){
                // console.log("pair = ", pair);
                // console.log("this.data_model.Message.moment = ", this.data_model.Message[pair[0]]);
                const label_name = pair[1];
                console.log("label_name = ", label_name);
                var label_element = this.svgobject.getElementById(label_name);
                console.log("label_element = ", label_element);
                label_element.textContent = this.data_model.Message[pair[0]].toFixed(2);

                //TODO убрать
                this.data_model.Message[pair[0]] += 1.0;

                var rect_element = this.svgobject.getElementById("rect_temperature1");
                // rect_element.style.fill = "red"; // РАБОТАЕТ
            }
        }


    },

    mounted() {

        // const dataObjectFromFile = require('example_kafka.json');
        fetch('example_kafka.json')
        .then((response) => {
            return response.json();
        })
        .then((json) => {
            this.data_model = json[0];
            // console.log("this.data_model = ", this.data_model);
        })
        .then(()=>{
            // console.log("this.data_model2 = ", this.data_model);
            // this.updateSVG();
        });

        
        

        setInterval(()=>{
            // for(var [key, ] of this.data_model.Message){
            //     this.data_model.Message[key] += 1;
            // }
            // this.xxx += 1;
            // this.sample_text_label.textContent = this.xxx;
            this.updateSVG();
        }, 1000);

        // this.svg = document.getElementById("svg2106").contentDocument;
        // console.log("svg = ", this.svg);
    },

    computed: {},
}
</script>
