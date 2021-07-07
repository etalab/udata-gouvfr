from flask import url_for, redirect
from udata.i18n import I18nBlueprint
from udata.api import api
from udata_gouvfr import theme


blueprint = I18nBlueprint('apidoc', __name__)


@blueprint.route('/api/')
@blueprint.route('/api/1/')
@api.documentation
def default_api():
    return redirect(url_for('apidoc.apidoc_index'))


@blueprint.route('/apidoc/')
def apidoc_index():
    return theme.render('apidoc.html')
