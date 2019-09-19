'use strict';

System.register(['./components/config'], function (_export, _context) {
    "use strict";

    var ExampleAppConfigCtrl;
    return {
        setters: [function (_componentsConfig) {
            ExampleAppConfigCtrl = _componentsConfig.ExampleAppConfigCtrl;
        }],
        execute: function () {
            _export('ConfigCtrl', ExampleAppConfigCtrl);
        }
    };
});