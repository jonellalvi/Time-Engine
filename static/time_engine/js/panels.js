var CC = {};

        CC.ItemList = function () {
            var count = 0;

            function make(templateItem) {
                var item = templateItem.cloneNode(true);
                item.classList.remove("template");
                item.classList.add("transitional");
                var r = item.getElementsByClassName("remove")[0];
                r.addEventListener("click", remove);
                var i = item.getElementsByClassName("insert")[0];
                i.addEventListener("click", insert);
                count++;

                document.getElementById("list").style.display="block";

                return  item;
            }

            function append() {
                console.log("append");
                __addBefore(CC.templateItem)
            }

            function __addBefore(selected) {
                var item = make(CC.templateItem);
                CC.list.insertBefore(item, selected);
                setTimeout(function () {
                    item.classList.remove("transitional")
                }, 0);
            }

            function insert(event) {
                __addBefore(event.target.parentElement);
            }

            function remove(event) {
                console.log("remove");
                console.log(event);
                event.target.parentElement.classList.add("transitional");
                console.log(event.target.parentElement.parentElement);
                count--;
                if (count === 0) {
                    event.target.parentElement.parentElement.style.display="none";
                }

                setTimeout(event.target.parentElement.remove, 3000);
            }

            return {
                append: append,
                insert: insert,
                remove: remove
            }
        }();

        window.addEventListener("load", function () {
            CC.list = document.getElementById("list");
            CC.templateItem = document.getElementsByClassName("template")[0];
        });

