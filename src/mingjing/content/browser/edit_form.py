from plone.dexterity.browser import edit
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('edit.pt')
