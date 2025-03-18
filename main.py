import logging
import os

import dotenv
from flask import Flask, jsonify

from theoriq import AgentDeploymentConfiguration, ExecuteContext, ExecuteResponse
from theoriq.api.v1alpha2.schemas import ExecuteRequestBody
from theoriq.biscuit import TheoriqCost
from theoriq.dialog import TextItemBlock
from theoriq.extra.flask.v1alpha2.flask import theoriq_blueprint
from theoriq.types import Currency

logger = logging.getLogger(__name__)

def execute(context: ExecuteContext, req: ExecuteRequestBody) -> ExecuteResponse:
    try:
        logger.info(
            f"Received request: {context.request_id} from {context.request_sender_type} {context.request_sender_address}"
        )

        # Get the last `TextItemBlock` from the Dialog
        last_block = req.last_item.blocks[0]
        text_value = last_block.data.text

        # Core implementation of the Agent
        agent_result = f"Hello {text_value} from a Theoriq Agent!"

        # Wrapping the result into an `ExecuteResponse` with some helper functions on the Context
        return context.new_response(
            blocks=[
                TextItemBlock(text=agent_result),
            ],
            cost=TheoriqCost(amount=1, currency=Currency.USDC),
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return context.runtime_error_response(str(e))

def create_app():
    app = Flask(__name__)

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Load agent configuration from env
    dotenv.load_dotenv()
    agent_config = AgentDeploymentConfiguration.from_env()

    # Create and register theoriq blueprint with v1alpha2 api version
    blueprint = theoriq_blueprint(agent_config, execute)
    app.register_blueprint(blueprint)

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("FLASK_PORT", 8000)))