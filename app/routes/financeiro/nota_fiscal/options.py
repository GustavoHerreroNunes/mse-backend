from . import nota_fiscal_bp

@nota_fiscal_bp.route('/', methods=['OPTIONS'])
@nota_fiscal_bp.route('/by_id/<int:nota_id>', methods=['OPTIONS'])
@nota_fiscal_bp.route('/by_etl/<int:etl_id>', methods=['OPTIONS'])
@nota_fiscal_bp.route('/export_csv', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
