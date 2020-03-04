export const help_button =  {view:"button", id: "help_button", css: "webix_transparent.webix_button",
	                                width: 40, type:"icon", icon: "mdi mdi-help-circle-outline"};


export function handleHelpPopup(buttonId, popupId, helpText) {
    if ($$(popupId) == undefined){
        webix.ui({
            view:"popup",
            id:popupId,
            body:{ template:helpText },
            position:function(state){
                var itempos = $$(buttonId).getNode().getBoundingClientRect()
                state.left = itempos.left + 10
                state.top = itempos.top + itempos.height
                state.width = 200; //relative values
                state.height = 80;
            }
        }).show();

        $$(popupId).attachEvent("onHide", function(){
            $$(popupId).destructor()
        })
    }
}