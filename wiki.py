# -*- coding: utf-8 -*-
"""
    wiki

    Wiki

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.wizard import Wizard, StateTransition, StateView, Button


class Wiki(ModelSQL, ModelView):
    'Wiki'
    _name = 'wiki.wiki'
    _description = __doc__

    title = fields.Char('Title', required=True
    )
    nereid_user = fields.Many2One(
        'nereid.user', 'Nereid User', required=True, select=True,
    )
    content = fields.Text("content")

    wiki_page = fields.One2Many("wiki.page", 'wiki', 'Wiki Page')

Wiki()

class WikiPage(ModelSQL, ModelView):
    'Wiki Page'
    _name = 'wiki.page'
    _description = __doc__

    wiki = fields.Many2One('wiki.wiki', 'Wiki', required=True)

    page_title = fields.Char('Page Title', required=True)

    content = fields.Text("Content")

    create_date = fields.DateTime("Created On")

WikiPage()

class WikiPageCreateStart(ModelView):
    'Wiki Page Create Start'
    _name = 'wiki.page.create.start'
    _description = __doc__

    nereid_user = fields.Many2One('nereid.user', 'Nereid User', required=True)
    page_title = fields.Char("Title", required=True)

WikiPageCreateStart()

class WikiPageCreate(Wizard):
    'Wiki Page Create'
    _name = 'wiki.page.create'
    _description = __doc__

    start = StateView(
        'wiki.page.create.start',
        'nereid_wiki.wiki_page_create_start_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Create', 'create_', 'tryton-ok')
        ]
    )

    create_ = StateTransition()

    def transition_create_(self, session):
        '''
        This method sets title for each wiki.
        '''
        wiki_obj = Pool().get('wiki.wiki')
        nereid_user_obj = Pool().get('nereid.user')

        nereid_user_ids = nereid_user_obj.search([])

        wiki_obj.create({
                'nereid_user': session.start.nereid_user.id,
                'title': session.start.page_title,
            })
        return 'end'

WikiPageCreate()

class WikiAccess(ModelSQL, ModelView):
    'Wiki Access'
    _name = 'wiki.access'
    _description = __doc__

    nereid_user_obj = Pool().get('nereid.user')
    wiki_page_obj = Pool().get('wiki.page')

    read = fields.Boolean('Private')
    write = fields.Boolean('public')

WikiAccess()
