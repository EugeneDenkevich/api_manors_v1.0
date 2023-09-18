from django.db.models import Count

from .models import *


def get_beds_and_rooms(response_data):
    """
    Calculate bads and rooms counts
    and make a dictionary in response data
    """
    if isinstance(response_data, dict):
        # For one object
        query_beds = Bed.objects.filter(
            object_id=response_data.get('id')).values(
            'type').annotate(Count('id')).order_by()
        query_rooms = Room.objects.filter(
            object_id=response_data.get('id')).values(
            'type').annotate(Count('id')).order_by()

        response_data['beds_types'] = []
        response_data['rooms_types'] = []
        for bed in query_beds:
            bed_type = dict(BEDS).get(bed.get('type'))
            id = 0
            for i in range(len(BEDS)):
                if BEDS[i][1] == bed_type:
                    id = i + 1
            response_data['beds_types'].append(
                {
                    'id': id,
                    'type': bed_type,
                    'count': bed.get('id__count'),
                }
            )
        for room in query_rooms:
            room_type = dict(ROOMS).get(room.get('type'))
            id = 0
            for i in range(len(BEDS)):
                if BEDS[i][1] == bed_type:
                    id = i + 1
            response_data['rooms_types'].append(
                {
                    'id': id,
                    'type': room_type,
                    'count': room.get('id__count'),
                }
            )
        return response_data
    # For all objects
    query_beds = Bed.objects.values(
        'type', 'object_id').annotate(Count('id')).order_by()
    query_rooms = Room.objects.values(
        'type', 'object_id').annotate(Count('id')).order_by()
    for object in response_data:
        object['beds_types'] = []
        object['rooms_types'] = []
        for bed in query_beds:
            if bed['object_id'] == object['id']:
                bed_type = dict(BEDS).get(bed.get('type'))
                id = 0
                for i in range(len(BEDS)):
                    if BEDS[i][1] == bed_type:
                        id = i + 1
                object['beds_types'].append(
                    {
                        'id': id,
                        'type': bed_type,
                        'count': bed.get('id__count'),
                    }
                )
        for room in query_rooms:
            if room['object_id'] == object['id']:
                room_type = dict(ROOMS).get(room.get('type'))
                id = 0
                for i in range(len(ROOMS)):
                    if ROOMS[i][1] == room_type:
                        id = i + 1
                object['rooms_types'].append(
                    {
                        'id': id,
                        'type': room_type,
                        'count': room.get('id__count'),
                    }
                )
    return response_data


def change_status(purchase):
    if purchase is None:
        return
    else:
        purchase.stat = 'Approved'
        purchase.save()
        print('here')
        house = purchase.object
        house.is_reserved = True
        house.save()



def finish_purchase(purchase):
    purchase.is_finished = True
    purchase.was_object = purchase.object
    purchase.stat = 'Closed'
    purchase.save()
    house = purchase.object
    purchase.object = None
    if not house.has_approved_purchases:
        house.is_reserved = False
    purchase.save()
    house.save()

def deny_purchase(purchase):
    if purchase is None:
        return
    else:
        purchase.is_finished = True
        purchase.was_object = purchase.object
        purchase.stat = 'Denied'
        purchase.save()
        house = purchase.object
        purchase.object = None
        if not house.has_approved_purchases:
            house.is_reserved = False
        purchase.save()
        house.save()
