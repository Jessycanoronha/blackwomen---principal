from flask import Blueprint, jsonify, request
from app.models.models import db, Woman, create_table_if_not_exists
import requests
from requests.exceptions import RequestException

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/sync-women', methods=['GET'])
def sync_women():
    try:
        url = 'https://theblackwomanhistory.firebaseio.com/.json'
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        content = data.get('content', {})
        teste = create_table_if_not_exists(Woman)
        if teste:
            for item in content:
                try:
                    woman = Woman.query.filter_by(id=item['id']).first()
                except Exception as e:
                    woman = None

                if not woman:
                    woman = Woman(
                        id=item['id'],
                        description=item['description'],
                        additional_metadata=item.get('metadata', {}),
                        order=item['order'],
                        slug=item['slug'],
                        title=item['title'],
                        country=item.get('metadata', {}).get('country'),
                        birthdate=item.get('metadata', {}).get('birthdate'),
                        deathdate=item.get('metadata', {}).get('deathdate'),
                        credits=item.get('metadata', {}).get('credits'),
                        image_url=item.get('metadata', {}).get('image',{}).get('url')
                    )
                    db.session.add(woman)
                else:
                    woman.description = item['description']
                    woman.additional_metadata = item.get('metadata', {})
                    woman.order = item['order']
                    woman.slug = item['slug']
                    woman.title = item['title']
                    woman.country = item.get('metadata', {}).get('country')
                    woman.birthdate = item.get('metadata', {}).get('birthdate')
                    woman.deathdate = item.get('metadata', {}).get('deathdate')
                    woman.credits = item.get('metadata', {}).get('credits')
                    woman.image_url = item.get('metadata', {}).get('image',{}).get('url')


                db.session.commit()

        return jsonify({'message': 'Figures synchronized successfully'}), 200

    except RequestException as e:
        return jsonify({'error': str(e)}), 500

    except KeyError as e:
        return jsonify({'error': f'Missing key in API response: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
