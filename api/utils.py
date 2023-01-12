from flask import jsonify

def generate_response(title, element):
    return jsonify({title: element.to_dict()})

def generate_list_response(title, elements):
    dicts = [element.to_dict() for element in elements] if elements else []
    return jsonify({title: dicts})