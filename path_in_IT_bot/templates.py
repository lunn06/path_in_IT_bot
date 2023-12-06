from jinja2.nativetypes import NativeEnvironment

env = NativeEnvironment()

meta_class_template = '''
class Meta_{{ class_id }}(StatesGroup):
{% for state_id in states %}
    state_{{ state_id }} = State()
{% endfor %}
'''

dialog_handler_template = '''
@router.message(Menu.interview)
@router.message(F.text == "{{ item.name }}")
async def dialog_{{ handler_id }}_handler(
    msg: Message, 
    user: DBUser, 
    dialog_manager: DialogManager
) -> None:
    for item in factory.items:
        if item.name == "{{ item.name }}":
            await dialog_manager.start(
                getattr(item.states, "state_{{ item.root.id }}"),
                data=item,
                mode=StartMode.RESET_STACK
            )
            break
'''

meta_class_env = env.from_string(meta_class_template)
dialog_handler_env = env.from_string(dialog_handler_template)
