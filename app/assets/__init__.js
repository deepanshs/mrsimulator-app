/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
 */

// local storage holds user configuration
console.log("store", window.localStorage.getItem("user-config"));
if (!window.localStorage.getItem("user-config")) {
  window.localStorage.setItem(
    "user-config",
    JSON.stringify({
      auto_update: true,
      // 'open_recent': [{'path': 'test'}],
      // 'number_of_sidebands': 12
    })
  );
}

// clear session storage on refresh
window.sessionStorage.clear();

var storeData = {
  previousIndex: 0,
  spin_system_index: 0,
  method_index: 0,
  data: { name: "", description: [], spin_systems: [], methods: [] },
};

var previous_timestamps = [-1, -1, -1, -1];
var last_li_scroll_index = 0;
let initial = 0;
// var createLists = function (spin_systems) {
//     var root = $('#spin-system-read-only');
//     var div = document.createElement('div');
//     div.className = 'display-form';
//     var ul = document.createElement('ul');
//     // ul.empty();
//     var li;
//     for (i = 0; i < spin_systems.length; i++) {
//         li = document.createElement("li");
//         li.innerHTML = update_info(spin_systems[i], i);
//         li.className = 'list-group-item';
//         ul.appendChild(li);
//         $(li).click(function (e) {
//             spinSystemOnClick(li);
//             e.preventDefault();
//         });
//     }
//     div.appendChild(ul);
//     root[0].appendChild(div);
// }

if (!window.dash_clientside) {
  window.dash_clientside = {};
}

window.dash_clientside.clientside = {
  initialize: function (n) {
    if (!window._user_init_) {
      init();
      window._user_init_ = {};
    }
    return null;
  },

  on_spin_systems_load: function (x, config) {
    storeData.data = JSON.parse(
      window.sessionStorage.getItem("local-mrsim-data")
    );
    let listomers = $("#spin-system-read-only div.display-form ul li");

    // Toggle classname to slide the contents on smaller screens
    let element = document.getElementById("iso-slide");
    if (element.classList.contains("iso-slide-offset")) {
      element.classList.toggle("iso-slide-offset");
      element.classList.toggle("iso-slide");
    }

    // Toggle classname to slide the contents on smaller screens
    if (listomers.length === 0) {
      element.classList.toggle("iso-slide-offset");
      element.classList.toggle("iso-slide");
    }

    default_li_action(listomers);

    // Add a fresh bind event to the list.
    listomers.each(function () {
      $(this).click(function (e) {
        spinSystemOnClick(this);
        e.preventDefault();
      });
      //   $(this).on('contextmenu', function(e) {
      //     alert('You\'ve tried to open context menu');
      //     e.preventDefault();
      //   });
    });

    // Select the entry at current index by initiating a click. If the current
    // index is greater then the length of the li, select 0;
    let index = get_spin_system_index();
    index = index >= listomers.length ? 0 : index;
    select_spin_system(listomers, index);
    return null;
  },

  on_methods_load: function (x, config) {
    storeData.data = JSON.parse(
      window.sessionStorage.getItem("local-mrsim-data")
    );
    let listomers = $("#method-read-only div.display-form ul li");

    // Toggle classname to slide the contents on smaller screens
    let element = document.getElementById("met-slide");
    if (element.classList.contains("met-slide-offset")) {
      element.classList.toggle("met-slide-offset");
      element.classList.toggle("met-slide");
    }

    // Toggle classname to slide the contents on smaller screens
    if (listomers.length === 0) {
      element.classList.toggle("met-slide-offset");
      element.classList.toggle("met-slide");
    }

    default_li_action(listomers);

    // Add a fresh bind event to the list.
    listomers.each(function () {
      let index = 0;
      $(this).click(function (e) {
        // method_on_click(this);
        default_li_item_action(this);

        // store the current-method-index in the session
        index = $(this).index();
        set_method_index(index);

        // Update the method fields
        window.methods.setFields(index);
        e.preventDefault();
      });
    });

    // Select the entry at current index by initiating a click. If the current
    // index is greater then the length of the li, select 0;
    let index = get_method_index();
    index = index >= listomers.length ? 0 : index;
    select_method(listomers, index);
    return null;
  },

  submit: function () {
    return storeData.data;
  },

  create_json: function () {
    // n1 is the trigger time for apply spin-system changes.
    // n2 is the trigger time for add new spin-system.
    // n3 is the trigger time for duplicate spin-system.
    // n4 is the trigger time for delete spin-system.
    let max_index, l, new_val, i;
    let new_list = [];

    for (i = 0; i < 4; i++) {
      if (arguments[i] == null) {
        new_list.push(-1);
      } else {
        new_list.push(arguments[i]);
      }
    }

    console.log("previous_timestamps", previous_timestamps);
    console.log("new_list", new_list);
    console.log("equal?", checkArrayEquality(new_list, previous_timestamps));

    let max_value = Math.max(...new_list);
    if (max_value === -1 && initial === 0) {
      initial = 1;
      throw window.dash_clientside.PreventUpdate;
    }

    if (checkArrayEquality(new_list, previous_timestamps)) {
      max_index = 0;
    } else {
      previous_timestamps = new_list;
      max_index = new_list.indexOf(max_value);
    }

    let data = storeData.data;

    l = data.spin_systems.length;
    let result = {};
    if (max_index === 0) {
      // modify
      result.data = extract_site_object_from_fields();
      result.index = get_spin_system_index();
      result.operation = "modify";
      // if (checkObjectEquality(result.data, data.spin_systems[result.index])) {
      //   throw window.dash_clientside.PreventUpdate;
      // }
      // data.spin_systems[result.index] = result.data;
    }
    if (max_index === 1) {
      // add
      result.data = {
        name: `Spin system ${l}`,
        description: "",
        abundance: 1,
        sites: [{ isotope: "1H", isotropic_chemical_shift: 0 }],
      };
      result.index = l;
      result.operation = "add";
      result.time = Date.now();
      set_spin_system_index(l);
    }
    if (max_index === 2) {
      // duplicate
      checkForEmptyListForOperation("copy", "spin system", l);
      result.data = data.spin_systems[get_spin_system_index()];
      result.index = l;
      result.operation = "duplicate";
      set_spin_system_index(l);
    }
    if (max_index === 3) {
      // delete
      checkForEmptyListForOperation("delete", "spin system", l);
      new_val = get_spin_system_index();
      result.data = max_value;
      result.index = new_val;
      result.operation = "delete";
      new_val -= 1;
      new_val = new_val < 0 ? 0 : new_val;
      set_spin_system_index(new_val);
    }
    return result;
  },

  create_method_json: function (n1, n2, n3, n4, method_template) {
    // n1 is the trigger time for apply method changes.
    // n2 is the trigger time for add new method.
    // n3 is the trigger time for duplicate method.
    // n4 is the trigger time for delete method.
    console.log(n1, n2, n3, n4);
    let max, l, new_val;
    if (n1 == null && n2 == null && n3 == null && n4 == null) {
      throw window.dash_clientside.PreventUpdate;
    }
    if (n1 == null) {
      n1 = -1;
    }
    if (n2 == null) {
      n2 = -1;
    }
    if (n3 == null) {
      n3 = -1;
    }
    if (n4 == null) {
      n4 = -1;
    }

    max = Math.max(n1, n2, n3, n4);
    let data = storeData.data;

    l = data.methods.length;
    let result = {};
    if (n1 == max) {
      // modify
      result.data = window.methods.updateData();
      result.index = get_method_index();
      result.operation = "modify";
    }
    if (n2 == max) {
      // add
      result.data = method_template.method;
      result.index = l;
      result.operation = "add";
      result.time = Date.now();
      set_method_index(l);
    }
    if (n3 == max) {
      // duplicate
      checkForEmptyListForOperation("copy", "method", l);
      result.data = data.methods[get_method_index()];
      result.index = l;
      result.operation = "duplicate";
      set_method_index(l);
    }
    if (n4 == max) {
      // delete
      checkForEmptyListForOperation("delete", "method", l);
      new_val = get_method_index();
      result.data = n4;
      result.index = new_val;
      result.operation = "delete";
      new_val -= 1;
      new_val = new_val < 0 ? 0 : new_val;
      set_method_index(new_val);
    }
    return result;
  },

  selected_spin_system: function (clickData, map, decompose, method_index) {
    if (clickData == null) {
      throw window.dash_clientside.PreventUpdate;
    }
    let index = decompose ? clickData.points[0].curveNumber : null;

    let listomers = $("#spin-system-read-only div.display-form ul li");
    let length = listomers.length;

    if (index == null || index >= length) {
      throw window.dash_clientside.PreventUpdate;
    }
    // get the correct index from the mapping array
    index = map[method_index][index];
    // highlight the corresponding spin-system by initialing a click.
    listomers[index].click();

    return null;
  },

  openAdvancedModalWindow: function (n1, n2, is_open) {
    if (n1 == null && n2 == null) {
      throw window.dash_clientside.PreventUpdate;
    }
    if (n1 || n2) {
      return !is_open;
    }
    return is_open;
  },

  setAutoUpdateOption: function (n1) {
    if (n1 == null) {
      throw window.dash_clientside.PreventUpdate;
    }
    // console.log('switch', $('#auto-update'));
    let data = JSON.parse(window.localStorage.getItem("user-config"));
    data.auto_update = !data.auto_update;
    // console.log('data', data);
    window.localStorage.setItem("user-config", JSON.stringify(data));
  },
};

function checkForEmptyListForOperation(operation, list, l) {
  if (l === 0) {
    alert(
      `Cannot ${operation} ${list} from an empty list. Try adding a ${list} first.`
    );
    throw window.dash_clientside.PreventUpdate;
  }
}

var default_li_action = function (listomers) {
  // Clear all previous selections and unbind the click events on list and
  // buttons.
  listomers.each(function () {
    $(this).unbind("click");
  });
};

var default_li_item_action = function (obj) {
  var ul = obj.parentElement,
    element,
    i;

  for (i = 0; i < ul.childNodes.length; i++) {
    element = ul.childNodes[i];
    // Remove all highlights.
    element.classList.remove("active");
  }
  // Scroll to the selection.
  scrollTo(ul.parentElement.parentElement, obj.offsetTop - 50, 300, "vertical");
  // Highlight the selected list.
  obj.classList.toggle("active");
};

/* Creates a smooth scroll based on the selected index of li. */
function scrollTo(element, to, duration, direction) {
  if (direction === "vertical") {
    var start = element.scrollTop,
      change = to - start,
      currentTime = 0,
      increment = 20;

    var animateScroll = function () {
      currentTime += increment;
      var val = Math.easeInOutQuad(currentTime, start, change, duration);
      element.scrollTop = val;
      if (currentTime < duration) {
        setTimeout(animateScroll, increment);
      }
    };
  }
  if (direction === "horizontal") {
    var start = element.scrollLeft,
      change = to - start,
      currentTime = 0,
      increment = 20;

    var animateScroll = function () {
      currentTime += increment;
      var val = Math.easeInOutQuad(currentTime, start, change, duration);
      element.scrollLeft = val;
      if (currentTime < duration) {
        setTimeout(animateScroll, increment);
      }
    };
  }
  animateScroll();
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
