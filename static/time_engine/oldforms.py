 <form id="theForm" action="" method="post" class="">
                            {% csrf_token %}
                            {# Include the hidden fields #}
                            {% for hidden in form.hidden_fields %}
                                {{ hidden }}
                            {% endfor %}
                            {# Include the visible fields #}
                            {% for field in form.visible_fields %}
                               <div class="fieldWrapper">
                                    {# uncomment to display field errors #}
                                    {{field.errors }}
                                    {{ field.label_tag }} {{ field }}
                               </div>
                            {% endfor %}


                            <button id="reset">Reset</button>
                            <button id="run">Run</button>
                            {% if user.is_authenticated %}
                            <button id="save">Save</button>
                            {% else %}
                            <button id="save" disabled>Save</button>

                            {% endif %}
                        </form>