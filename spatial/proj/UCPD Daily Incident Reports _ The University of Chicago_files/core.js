// GSA jQuery plugin
(function($) {
    $.fn.GSASearch = function(options) {
        var defaults = {
            q: "",
            start: "",
            num: "15",
            sitesearch: "",
            site: "default_collection",
            waitGifPath: "/i/template/loading.gif",
            protocol: "http:"
        };
        var options = $.extend(defaults, options);
        var resultsContainer = $(this);
        resultsContainer.data("searchSiteURL", options.protocol + '//search.uchicago.edu');
        resultsContainer.data("startNumber", "1");
        resultsContainer.data("totalCount", "10");
        return this.each(function() {
            resultsContainer.empty();
            resultsContainer.html('<img src="' + options.waitGifPath + '" class="GSAwait">');
            options.q = options.q.replace(/(<([^>]+)>)/ig, "");
            options.start = options.start.toString().replace(/(<([^>]+)>)/ig, "");
            options.num = options.num.toString().replace(/(<([^>]+)>)/ig, "");
            options.sitesearch = options.sitesearch.replace(/(<([^>]+)>)/ig, "");
            options.site = options.site.replace(/(<([^>]+)>)/ig, "");
            search(options.q, options.start, options.num, options.sitesearch, options.site);
        });
        function search(q, start, num, sitesearch, site) {
            var Base64 = {
                _keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
                encode : function (input) {
                    var output = "";
                    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
                    var i = 0;
                    input = Base64._utf8_encode(input);
                    while (i < input.length) {
                        chr1 = input.charCodeAt(i++);
                        chr2 = input.charCodeAt(i++);
                        chr3 = input.charCodeAt(i++);
                        enc1 = chr1 >> 2;
                        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
                        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
                        enc4 = chr3 & 63;
                        if (isNaN(chr2)) {
                            enc3 = enc4 = 64;
                        } else if (isNaN(chr3)) {
                            enc4 = 64;
                        }
                        output = output + this._keyStr.charAt(enc1) + this._keyStr.charAt(enc2) + this._keyStr.charAt(enc3) + this._keyStr.charAt(enc4);
                    }
                    return output;
                },
                decode : function (input) {
                    var output = "";
                    var chr1, chr2, chr3;
                    var enc1, enc2, enc3, enc4;
                    var i = 0;
                    input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
                    while (i < input.length) {
                        enc1 = this._keyStr.indexOf(input.charAt(i++));
                        enc2 = this._keyStr.indexOf(input.charAt(i++));
                        enc3 = this._keyStr.indexOf(input.charAt(i++));
                        enc4 = this._keyStr.indexOf(input.charAt(i++));
                        chr1 = (enc1 << 2) | (enc2 >> 4);
                        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                        chr3 = ((enc3 & 3) << 6) | enc4;
                        output = output + String.fromCharCode(chr1);
                        if (enc3 != 64) {
                            output = output + String.fromCharCode(chr2);
                        }
                        if (enc4 != 64) {
                            output = output + String.fromCharCode(chr3);
                        }
                    }
                    output = Base64._utf8_decode(output);
                    return output;
                },
                _utf8_encode : function (string) {
                    string = string.replace(/\r\n/g, "\n");
                    var utftext = "";
                    for (var n = 0; n < string.length; n++) {
                        var c = string.charCodeAt(n);
                        if (c < 128) {
                            utftext += String.fromCharCode(c);
                        } else if ((c > 127) && (c < 2048)) {
                            utftext += String.fromCharCode((c >> 6) | 192);
                            utftext += String.fromCharCode((c & 63) | 128);
                        } else {
                            utftext += String.fromCharCode((c >> 12) | 224);
                            utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                            utftext += String.fromCharCode((c & 63) | 128);
                        }
                    }
                    return utftext;
                },
                _utf8_decode : function (utftext) {
                    var string = "";
                    var i = 0;
                    var c = c1 = c2 = 0;
                    while ( i < utftext.length ) {
                        c = utftext.charCodeAt(i);
                        if (c < 128) {
                            string += String.fromCharCode(c);
                            i++;
                        } else if ((c > 191) && (c < 224)) {
                            c2 = utftext.charCodeAt(i + 1);
                            string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                            i += 2;
                        } else {
                            c2 = utftext.charCodeAt(i + 1);
                            c3 = utftext.charCodeAt(i + 2);
                            string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                            i += 3;
                        }
                    }
                    return string;
                }
            };
            var searchParams = '&q=' + escape(q) + '&start=' + escape(start) + '&sitesearch=' + escape(sitesearch) + '&site=' + escape(site);
            searchParams += '&filter=0';
            var jsonParams = 'btnG=Search&entqr=0&ud=1&sort=date%3AD%3AL%3Ad1&output=xml_no_dtd&oe=UTF-8&ie=UTF-8' + '&client=default_frontend&proxystylesheet=jsonp_frontend' + searchParams + '&num=' + escape(num);
            var searchSiteURL = options.protocol + '//search.uchicago.edu/search?btnG=Search&entqr=0&ud=1&sort=date:D:L:d1&output=xml_no_dtd&oe=UTF-8&ie=UTF-8&client=default_frontend&proxystylesheet=default_frontend' + searchParams;
            var proxyUrl = options.protocol + '//webresources.uchicago.edu/php/proxy/gsaproxy.php?encodedParams=' + Base64.encode(jsonParams) + '&callback=?';
            resultsContainer.data("searchSiteURL", searchSiteURL);
            var fetchSuccess = 0;
            var jqxhr = $.getJSON(proxyUrl, function(data) {
                showResults(data);
                fetchSuccess = 1;
            });
            if (jqxhr != undefined) {
                jqxhr.error(function() {
                    showError();
                });
            } else {
                setTimeout(function() {
                    if (!fetchSuccess) {
                        showError();
                    }
                }, 7000);
            }
        }
        function showError() {
            var message = 'There is a problem fetching search results. Please refresh the page or contact <a href="mailto:weberror@uchicago.edu">weberror@uchicago.edu</a>.';
            resultsContainer.html(message);
            resultsContainer.data("totalCount", 0);
            resultsContainer.trigger('GSASearchComplete');
        }
        function showResults(data) {
            var startNumber, totalCount = 0;
            var res = '<h2>You searched for: “' + data.GSP.Q + '”</h2>';
            if (data.GSP.RES == undefined) {
                res += '<p>No pages were found.</p>';
            } else {
                res += '<p><strong>Results ' + data.GSP.RES.SN + '–' + data.GSP.RES.EN + ' of about ' + data.GSP.RES.M + '.</strong></p>';
                var thisResultCount = data.GSP.RES.EN - data.GSP.RES.SN + 1;
                if (thisResultCount == 1) {
                    var result = data.GSP.RES.R;
                    if ( result['S'] == null ) {
                        result['S'] = '';
                    }
                    var resultStr = '<h3><a href="' + result['U'] + '">' + result['T'] + '</a></h3>';
                    resultStr += '<p>' + result['S'] + '<br class="url"><em><a href="' + result['U'] + '">' + result['U'] + '</a></em></p>';
                    res += resultStr;
                } else {
                    for (var i = 0; i < thisResultCount; i++) {
                        var result = data.GSP.RES.R[i];
                        if ( result['S'] == null ) {
                            result['S'] = '';
                        }
                        var resultStr = '<h3><a href="' + result['U'] + '">' + result['T'] + '</a></h3>';
                        resultStr += '<p>' + result['S'] + '<br class="url"><em><a href="' + result['U'] + '">' + result['U'] + '</a></em></p>';
                        res += resultStr;
                    }
                }
                var perPageCount = options.num;
                startNumber = data.GSP.RES.SN;
                totalCount = (thisResultCount < perPageCount) ? data.GSP.RES.EN : data.GSP.RES.M;
            }
            resultsContainer.html(res);
            resultsContainer.data("startNumber", startNumber);
            resultsContainer.data("totalCount", totalCount);
            resultsContainer.trigger('GSASearchComplete');
            $('.maincontent br').not('.url').replaceWith(' ');
        }
    };
})(jQuery);
//jQuery pager
(function($) {
    $.fn.pager = function(options) {
        var opts = $.extend({}, $.fn.pager.defaults, options);
        return this.each(function() {
            $(this).empty().append(renderpager(parseInt(options.pagenumber), parseInt(options.pagecount), options.buttonClickCallback));
        });
    };
    function renderpager(pagenumber, pagecount, buttonClickCallback) {
        var $pager = $('<ul></ul>');
        $pager.append(renderButton('first', pagenumber, pagecount, buttonClickCallback));
        var startPoint = 1;
        var endPoint = 9;
        if (pagenumber > 4) {
            startPoint = pagenumber - 4;
            endPoint = pagenumber + 4;
        }
        if (endPoint > pagecount) {
            startPoint = pagecount - 8;
            endPoint = pagecount;
        }
        if (startPoint < 1) {
            startPoint = 1;
        }
        for (var page = startPoint; page <= endPoint; page++) {
            var currentButton = $('<li>' + (page) + '</li>');
            page == pagenumber ? currentButton.addClass('active') : currentButton.bind('click focusin', function() {
                buttonClickCallback(this.firstChild.data);
            });
            currentButton.appendTo($pager);
        }
        $pager.append(renderButton('last', pagenumber, pagecount, buttonClickCallback));
        return $pager;
    }
    function renderButton(buttonLabel, pagenumber, pagecount, buttonClickCallback) {
        var $Button = $('<li>' + buttonLabel + '</li>');
        var destPage = 1;
        switch (buttonLabel) {
        case "first":
            destPage = 1;
            break;
        case "last":
            destPage = pagecount;
            break;
        }
        if (buttonLabel == "first") {
            pagenumber <= 1 ? $Button : $Button.bind('click focusin', function() {
                buttonClickCallback(destPage);
            });
        } else {
            pagenumber >= pagecount ? $Button : $Button.bind('click focusin', function() {
                buttonClickCallback(destPage);
            });
        }
        return $Button;
    }
    $.fn.pager.defaults = {
        pagenumber: 1,
        pagecount: 1
    };
})(jQuery);
// custom search results
$(document).ready(function() {
    function submitSearch(searchTerm) {
        linkDiv = $("#GSALink");
        pagerDiv = $("#GSAPager");
        resultsDiv = $("#GSAResults");
        thisQ = searchTerm;
        perPageCount = 15;
        linkDiv.empty();
        pagerDiv.empty();
        resultsDiv.GSASearch({
            q: thisQ,
            num: perPageCount,
            sitesearch: "safety-security.uchicago.edu"
        });
    }
    function searchTermFromQString() {
        var s;
        queryString = window.location.search.substring(1);
        nameValPairs = queryString.split("&");
        for (i = 0; i < nameValPairs.length; i++) {
            nameVal = nameValPairs[i].split("=");
            if (nameVal[0] == "GSAq")
                s = nameVal[1];
        }
        return s;
    }
    var searchTerm = searchTermFromQString();
    if (searchTermFromQString() != undefined) {
        searchTerm = unescape(searchTerm);
        submitSearch(searchTerm);
    }
    $("#GSAResults, #GSAResultsFS2").bind("GSASearchComplete", function() {
        pagerDiv = $("#GSAPager");
        perPageCount = 15;
        resultsDiv = $(this);
        pagerDiv.empty();
        thisPageNumber = Math.floor((parseInt(resultsDiv.data("startNumber")) + parseInt(perPageCount)) / parseInt(perPageCount));
        thisPageCount = Math.ceil(parseInt(resultsDiv.data("totalCount")) / perPageCount);
        pagerDiv.pager({
            pagenumber: thisPageNumber,
            pagecount: thisPageCount,
            buttonClickCallback: PagerClick
        });
    });
    PagerClick = function(pageclickednumber) {
        resultsDiv = $("#GSAResults");
        perPageCount = 15;
        startNumber = (pageclickednumber * perPageCount) - perPageCount;
        resultsDiv.GSASearch({
            q: searchTerm,
            start: startNumber,
            num: perPageCount,
            sitesearch: "safety-security.uchicago.edu"
        });
    }
});
/* =============================================================
 * bootstrap-collapse.js v2.3.2
 * http://getbootstrap.com/2.3.2/javascript.html#collapse
 * =============================================================
 * Copyright 2013 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================ */


!function ($) {

  "use strict"; // jshint ;_;


 /* COLLAPSE PUBLIC CLASS DEFINITION
  * ================================ */

  var Collapse = function (element, options) {
    this.$element = $(element)
    this.options = $.extend({}, $.fn.collapse.defaults, options)

    if (this.options.parent) {
      this.$parent = $(this.options.parent)
    }

    this.options.toggle && this.toggle()
  }

  Collapse.prototype = {

    constructor: Collapse

  , dimension: function () {
      var hasWidth = this.$element.hasClass('width')
      return hasWidth ? 'width' : 'height'
    }

  , show: function () {
      var dimension
        , scroll
        , actives
        , hasData

      if (this.transitioning || this.$element.hasClass('in')) return

      dimension = this.dimension()
      scroll = $.camelCase(['scroll', dimension].join('-'))
      actives = this.$parent && this.$parent.find('> .accordion-group > .in')

      if (actives && actives.length) {
        hasData = actives.data('collapse')
        if (hasData && hasData.transitioning) return
        actives.collapse('hide')
        hasData || actives.data('collapse', null)
      }

      this.$element[dimension](0)
      this.transition('addClass', $.Event('show'), 'shown')
      $.support.transition && this.$element[dimension](this.$element[0][scroll])
    }

  , hide: function () {
      var dimension
      if (this.transitioning || !this.$element.hasClass('in')) return
      dimension = this.dimension()
      this.reset(this.$element[dimension]())
      this.transition('removeClass', $.Event('hide'), 'hidden')
      this.$element[dimension](0)
    }

  , reset: function (size) {
      var dimension = this.dimension()

      this.$element
        .removeClass('collapse')
        [dimension](size || 'auto')
        [0].offsetWidth

      this.$element[size !== null ? 'addClass' : 'removeClass']('collapse')

      return this
    }

  , transition: function (method, startEvent, completeEvent) {
      var that = this
        , complete = function () {
            if (startEvent.type == 'show') that.reset()
            that.transitioning = 0
            that.$element.trigger(completeEvent)
          }

      this.$element.trigger(startEvent)

      if (startEvent.isDefaultPrevented()) return

      this.transitioning = 1

      this.$element[method]('in')

      $.support.transition && this.$element.hasClass('collapse') ?
        this.$element.one($.support.transition.end, complete) :
        complete()
    }

  , toggle: function () {
      this[this.$element.hasClass('in') ? 'hide' : 'show']()
    }

  }


 /* COLLAPSE PLUGIN DEFINITION
  * ========================== */

  var old = $.fn.collapse

  $.fn.collapse = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('collapse')
        , options = $.extend({}, $.fn.collapse.defaults, $this.data(), typeof option == 'object' && option)
      if (!data) $this.data('collapse', (data = new Collapse(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.collapse.defaults = {
    toggle: true
  }

  $.fn.collapse.Constructor = Collapse


 /* COLLAPSE NO CONFLICT
  * ==================== */

  $.fn.collapse.noConflict = function () {
    $.fn.collapse = old
    return this
  }


 /* COLLAPSE DATA-API
  * ================= */

  $(document).on('click.collapse.data-api', '[data-toggle=collapse]', function (e) {
    var $this = $(this), href
      , target = $this.attr('data-target')
        || e.preventDefault()
        || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') //strip for ie7
      , option = $(target).data('collapse') ? 'toggle' : $this.data()
    $this[$(target).hasClass('in') ? 'addClass' : 'removeClass']('collapsed')
    $(target).collapse(option)
  })

}(window.jQuery);

/*Lazy Load - jQuery plugin for lazy loading images // Copyright (c) 2007-2013 Mika Tuupola // Licensed under the MIT license: // http://www.opensource.org/licenses/mit-license.php // Project home: http://www.appelsiini.net/projects/lazyload // Version: 1.8.4*/
(function(a, b, c, d) {
    var e = a(b);
    a.fn.lazyload = function(c) {
        function i() {
            var b = 0;
            f.each(function() {
                var c = a(this);
                if (h.skip_invisible&&!c.is(":visible"))
                    return;
                if (!a.abovethetop(this, h)&&!a.leftofbegin(this, h))
                    if (!a.belowthefold(this, h)&&!a.rightoffold(this, h))
                        c.trigger("appear"), b = 0;
                else if (++b > h.failure_limit)
                    return !1
            })
        }
        var f = this, g, h = {
            threshold: 0,
            failure_limit: 0,
            event: "scroll",
            effect: "show",
            container: b,
            data_attribute: "original",
            skip_invisible: !0,
            appear: null,
            load: null
        };
        return c && (d !== c.failurelimit && (c.failure_limit = c.failurelimit, delete c.failurelimit), d !== c.effectspeed && (c.effect_speed = c.effectspeed, delete c.effectspeed), a.extend(h, c)), g = h.container === d || h.container === b ? e : a(h.container), 0 === h.event.indexOf("scroll") && g.bind(h.event, function(a) {
            return i()
        }), this.each(function() {
            var b = this, c = a(b);
            b.loaded=!1, c.one("appear", function() {
                if (!this.loaded) {
                    if (h.appear) {
                        var d = f.length;
                        h.appear.call(b, d, h)
                    }
                    a("<img />").bind("load", function() {
                        c.hide().attr("src", c.data(h.data_attribute))[h.effect](h.effect_speed), b.loaded=!0;
                        var d = a.grep(f, function(a) {
                            return !a.loaded
                        });
                        f = a(d);
                        if (h.load) {
                            var e = f.length;
                            h.load.call(b, e, h)
                        }
                    }).attr("src", c.data(h.data_attribute))
                }
            }), 0 !== h.event.indexOf("scroll") && c.bind(h.event, function(a) {
                b.loaded || c.trigger("appear")
            })
        }), e.bind("resize", function(a) {
            i()
        }), /iphone|ipod|ipad.*os 5/gi.test(navigator.appVersion) && e.bind("pageshow", function(b) {
            b.originalEvent.persisted && f.each(function() {
                a(this).trigger("appear")
            })
        }), a(b).load(function() {
            i()
        }), this
    }, a.belowthefold = function(c, f) {
        var g;
        return f.container === d || f.container === b ? g = e.height() + e.scrollTop() : g = a(f.container).offset().top + a(f.container).height(), g <= a(c).offset().top - f.threshold
    }, a.rightoffold = function(c, f) {
        var g;
        return f.container === d || f.container === b ? g = e.width() + e.scrollLeft() : g = a(f.container).offset().left + a(f.container).width(), g <= a(c).offset().left - f.threshold
    }, a.abovethetop = function(c, f) {
        var g;
        return f.container === d || f.container === b ? g = e.scrollTop() : g = a(f.container).offset().top, g >= a(c).offset().top + f.threshold + a(c).height()
    }, a.leftofbegin = function(c, f) {
        var g;
        return f.container === d || f.container === b ? g = e.scrollLeft() : g = a(f.container).offset().left, g >= a(c).offset().left + f.threshold + a(c).width()
    }, a.inviewport = function(b, c) {
        return !a.rightoffold(b, c)&&!a.leftofbegin(b, c)&&!a.belowthefold(b, c)&&!a.abovethetop(b, c)
    }, a.extend(a.expr[":"], {
        "below-the-fold": function(b) {
            return a.belowthefold(b, {
                threshold: 0
            })
        },
        "above-the-top": function(b) {
            return !a.belowthefold(b, {
                threshold: 0
            })
        },
        "right-of-screen": function(b) {
            return a.rightoffold(b, {
                threshold: 0
            })
        },
        "left-of-screen": function(b) {
            return !a.rightoffold(b, {
                threshold: 0
            })
        },
        "in-viewport": function(b) {
            return a.inviewport(b, {
                threshold: 0
            })
        },
        "above-the-fold": function(b) {
            return !a.belowthefold(b, {
                threshold: 0
            })
        },
        "right-of-fold": function(b) {
            return a.rightoffold(b, {
                threshold: 0
            })
        },
        "left-of-fold": function(b) {
            return !a.rightoffold(b, {
                threshold: 0
            })
        }
    })
})(jQuery, window, document)

// Lazyload images
    $('img.lazy').show().lazyload({
        effect: 'fadeIn',
        threshold: 20
    });

    $('img.lazy-q').show().lazyload({
        effect: 'fadeIn',
    });