<form id="theForm" action="" method="post" class="">
                            {% csrf_token %}
                            <!--{# {{ form.as_p }} #}-->
                            {% for field in form %}
                                <div class="fieldWrapper">
                                    {# uncomment to display field errors #}
                                    {# {{field.errors }} #}
                                    <tr>
                                        <td>{{ field.label_tag }}<span class="red">*</span></td>
                                        <td>{{ field }}</td>
                                        <td id="{{ field.id_for_label }}Error" class="red">&nbsp;</td>
                                    </tr>
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

 <div class="fieldWrapper"><!--Sunday-->
                                {{ form.has_sunday.errors }}
                                <div class="checkboxes">
                                    {{ form.has_sunday }}
                                    <label for="{{ form.has_sunday.id_for_label }}">S</label>
                                </div>
                            </div>
                            <div class="fieldWrapper"><!--Monday-->
                                {{ form.has_monday.errors }}
                                <div class="checkboxes">
                                    {{ form.has_monday }}
                                    <label for="{{ form.has_monday.id_for_label }}">M</label>
                                </div>
                            </div>