# qc-midi-tool

hyper specific tool for my use case with the quad cortex

i wanted to advance through a setlist with a single button using an external midi controller, this apparently is not an implemented behavior on the QC (for some godforesaken reason) so i just did it myself

in my case i used an iconnectivity mio to take in my soleman foot controller and output to my QC via DIN, you can adjust your inport and outport as necessary. all this app does is override CC#0 and sends an accompanying PC message to iterate through your selected setlist, passing through any other messages so that i can still use my expression pedal and footswitch/scene controls. this allows me to throw down my cheap soleman controller and keep my QC safely offstage.