'use strict';

System.register(['lodash'], function (_export, _context) {
    "use strict";

    var _, _createClass, ExampleAppConfigCtrl;

    function _classCallCheck(instance, Constructor) {
        if (!(instance instanceof Constructor)) {
            throw new TypeError("Cannot call a class as a function");
        }
    }

    return {
        setters: [function (_lodash) {
            _ = _lodash.default;
        }],
        execute: function () {
            _createClass = function () {
                function defineProperties(target, props) {
                    for (var i = 0; i < props.length; i++) {
                        var descriptor = props[i];
                        descriptor.enumerable = descriptor.enumerable || false;
                        descriptor.configurable = true;
                        if ("value" in descriptor) descriptor.writable = true;
                        Object.defineProperty(target, descriptor.key, descriptor);
                    }
                }

                return function (Constructor, protoProps, staticProps) {
                    if (protoProps) defineProperties(Constructor.prototype, protoProps);
                    if (staticProps) defineProperties(Constructor, staticProps);
                    return Constructor;
                };
            }();

            _export('ExampleAppConfigCtrl', ExampleAppConfigCtrl = function () {
                function ExampleAppConfigCtrl(backendSrv) {
                    var _this = this;

                    _classCallCheck(this, ExampleAppConfigCtrl);

                    this.backendSrv = backendSrv;
                    this.datasourceName = 'ES stagemonitor';
                    this.isDatasourceCreated = false;
                    this.appEditCtrl.setPreUpdateHook(this.preUpdate.bind(this));

                    this.appModel.jsonData = this.appModel.jsonData || {};
                    this.appModel.jsonData.elasticsearchUrl = this.appModel.jsonData.elasticsearchUrl || "";
                    this.appModel.jsonData.reportingInterval = this.appModel.jsonData.reportingInterval || ">60s";
                    this.validation = {
                        reportingIntervalValid: true,
                        elasticsearchUrlValid: true
                    };

                    backendSrv.get('/public/plugins/stagemonitor-grafana-elasticsearch/plugin.json').then(function (data) {
                        _this.dashboards = _.filter(data.includes, { type: 'dashboard' });
                    });
                }

                _createClass(ExampleAppConfigCtrl, [{
                    key: 'preUpdate',
                    value: function preUpdate() {
                        if (this.isDatasourceCreated) {
                            return Promise.resolve();
                        } else {
                            return this.createDatasource();
                        }
                    }
                }, {
                    key: 'init',
                    value: function init() {
                        var _this2 = this;

                        this.backendSrv.get('/api/datasources').then(function (datasources) {
                            _this2.isDatasourceCreated = _.findIndex(datasources, { name: _this2.datasourceName }) !== -1;
                        });
                    }
                }, {
                    key: 'createDatasource',
                    value: function createDatasource() {

                        this.validation.elasticsearchUrlValid = !this.isEmptyOrUndefined(this.appModel.jsonData.elasticsearchUrl);
                        this.validation.reportingIntervalValid = !this.isEmptyOrUndefined(this.appModel.jsonData.reportingInterval);

                        if (_.values(this.validation).some(function (value) {
                            return !value;
                        })) {
                            return Promise.reject();
                        } else {
                            return this.backendSrv.post('/api/datasources', {
                                "name": this.datasourceName,
                                "type": "elasticsearch",
                                "url": this.appModel.jsonData.elasticsearchUrl,
                                "access": "proxy",
                                "jsonData": {
                                    "timeField": "@timestamp",
                                    "esVersion": 2, "interval": "Daily",
                                    "timeInterval": this.appModel.jsonData.reportingInterval
                                },
                                "database": "[stagemonitor-metrics-]YYYY.MM.DD"
                            });
                        }
                    }
                }, {
                    key: 'isEmptyOrUndefined',
                    value: function isEmptyOrUndefined(value) {
                        return value === undefined || value == null || value.trim() === "";
                    }
                }]);

                return ExampleAppConfigCtrl;
            }());

            _export('ExampleAppConfigCtrl', ExampleAppConfigCtrl);

            ExampleAppConfigCtrl.templateUrl = 'components/config.html';
        }
    };
});