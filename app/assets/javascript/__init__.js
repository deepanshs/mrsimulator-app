/*
 * Author = "Deepansh J. Srivastava"
 * Email = "srivastava.89@osu.edu"
 */

/* jshint esversion: 6 */

// local storage holds user configuration
console.log("store", window.localStorage.getItem("user-config"));
if (!window.localStorage.getItem("user-config")) {
  window.localStorage.setItem(
    "user-config",
    JSON.stringify({
      auto_update: false,
      // 'open_recent': [{'path': 'test'}],
      // 'number_of_sidebands': 12
    })
  );
}

var storeData = {
  previousIndex: 0,
  spin_system_index: 0,
  method_index: 0,
  data: {
    simulator: {
      name: "",
      description: [],
      spin_systems: [],
      methods: [],
    },
  },
};
var hasInitialized = false;

if (!window.dash_clientside) {
  window.dash_clientside = {};
}

window.dash_clientside.clientside = {
  initialize: function (n) {
    // clear session storage on refresh
    if (window.sessionStorage) window.sessionStorage.clear();

    if (!hasInitialized) {
      storeData.spin_system_index = 0;
      storeData.method_index = 0;
      hasInitialized = true;
    }

    init();
    activateMethodTools();
    activateSystemTools();

    return null;
  },

  onReload: function (data) {
    storeData.data = data;
    _onFeaturesReload();
    _onSpinSystemsLoad();
    _onMethodsLoad();
    _refreshTables();
  },

  downloadSession: function (n, data) {
    if (n === null) {
      throw window.dash_clientside.PreventUpdate;
    }
    if (data === null) {
      throw window.dash_clientside.PreventUpdate;
    }

    // prepare the download.
    let dataStr = "data:text/json;charset=utf-8,";
    dataStr += encodeURIComponent(JSON.stringify(data));

    let dlAnchorElem = document.getElementById("download-session-link");
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", "session.mrsim");
    dlAnchorElem.click();

    dataStr = ndlAnchorElem = null;
    return "";
  },
};

function ctxTriggerID() {
  return dash_clientside.callback_context.triggered.map((t) => t.prop_id);
}

function ctxTriggerStates() {
  return dash_clientside.callback_context.states;
}

function checkForEmptyListBeforeOperation(operation, list, l) {
  if (l === 0) {
    alert(
      `Cannot ${operation} ${list} from an empty list. Try adding a ${list} first.`
    );
    throw window.dash_clientside.PreventUpdate;
  }
}

/* Creates a smooth scroll based on the selected index of li. */
function scrollTo(element, to, duration, direction) {
  var start, change, currentTime, increment, animateScroll;
  if (direction === "vertical") {
    start = element.scrollTop;
    change = to - start;
    currentTime = 0;
    increment = 20;

    animateScroll = function () {
      currentTime += increment;
      let val = Math.easeInOutQuad(currentTime, start, change, duration);
      element.scrollTop = val;
      if (currentTime < duration) {
        setTimeout(animateScroll, increment);
      }
    };
    animateScroll();
  }

  if (direction === "horizontal") {
    start = element.scrollLeft;
    change = to - start;
    currentTime = 0;
    increment = 20;

    animateScroll = function () {
      currentTime += increment;
      let val = Math.easeInOutQuad(currentTime, start, change, duration);
      element.scrollLeft = val;
      if (currentTime < duration) {
        setTimeout(animateScroll, increment);
      }
    };
    animateScroll();
  }
}

// t = current time
// b = start value
// c = change in value
// d = duration
Math.easeInOutQuad = function (t, b, c, d) {
  t /= d / 2;
  if (t < 1) return (c / 2) * t * t + b;
  t--;
  return (-c / 2) * (t * (t - 2) - 1) + b;
};

var contextMenu = function () {
  return `<nav class="context-menu">
        <ul class="context-menu__items">
        <li class="context-menu__item">
            <a href="#" class="context-menu__link">
            <i class="fa fa-eye"></i> View Task
            </a>
        </li>
        <li class="context-menu__item">
            <a href="#" class="context-menu__link">
            <i class="fa fa-edit"></i> Edit Task
            </a>
        </li>
        <li class="context-menu__item">
            <a href="#" class="context-menu__link">
            <i class="fa fa-times"></i> Delete Task
            </a>
        </li>
        </ul>
    </nav>`;
};

var darkMode = function () {
  let element = document.body;
  element.classList.toggle("dark-mode");
};
