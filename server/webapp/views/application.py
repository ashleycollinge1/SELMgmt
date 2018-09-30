from flask import Flask, jsonify
import winrm

@app.route('/client/<hostname>/install/<application>')
def install_application(hostname, application):
	"""
	Takes hostname and application name to start an async task
	which will remotely install the application on the specified
	host.
	Support applications:

	Success:
	200
	Example: {'message': {
							'task_id': 2,
							'hostname': sel0516,
							'application_name': 'FoxitPDFReader'
						}
			}
	"""




	return jsonify({'message': {'task_id': task_id,
								'hostname': hostname,
								'application_name': application_name}})