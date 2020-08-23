from db.database import Database
import sys
sys.path.append("..")

# Connect to database
database = Database()


class MessageFilter:

    @staticmethod
    def get_filter(filter_id):
        filter = database.get_filter(filter_id)
        if filter is None:
            return False

        filter_dict = {
            'id': filter[0],
            'audio': filter[1],
            'video': filter[2],
            'photo': filter[3],
            'sticker': filter[4],
            'document': filter[5],
            'hashtag': filter[6],
            'link': filter[7],
            'contain': filter[8],
            'notcontain': filter[9]
        }
        return filter_dict

    @staticmethod
    def get_active_filters(filter_dict):
        """
        Takes in a filter dictionary
        Returns a list of active filter names
        Example: ('photo', 'audio')
        """
        if not isinstance(filter_dict, dict):
            raise ValueError('Provide a dictionary')

        active_filter_list = []
        for key, value in filter_dict.items():
            if value != 0 and value is not None:
                if key != 'id':
                    active_filter_list.append(key)

        return active_filter_list

    @staticmethod
    def get_message_type(event):

        # Photos Messages
        if hasattr(event.media, 'photo'):
            return 'photo'

        # Look for links and hashtags in event.entities
        if event.entities is not None:
            for entity in event.entities:
                entity_name = type(entity).__name__

                if entity_name == 'MessageEntityHashtag':
                    return 'hashtag'

                if entity_name == 'MessageEntityUrl':
                    return 'link'

        # Text Messages
        if event.media == None:
            return 'text'

        # Documents (audio, video, sticker, files)
        mime_type = event.media.document.mime_type
        if 'audio' in mime_type:
            return 'audio'
        if 'video' in mime_type:
            return 'video'
        if 'image/webp' in mime_type:
            return 'sticker'

        # Anything else is a file
        return 'document'

    @staticmethod
    def filter_msg(filter_id, message_event):
        """
        Function that decides if a message should be forwarded or not
        Returns Boolean
        """

        # Get Filter dictionary from database
        filter_dict = MessageFilter.get_filter(filter_id)
        if filter_dict == False:
            print('No filters for id : {}'.format(filter_id))
            return False

        # Get Active Filter list
        filter_list = MessageFilter.get_active_filters(filter_dict)

        # Get Message Types
        msg_type = MessageFilter.get_message_type(message_event)
        msg_text = message_event.message.text.lower()

        if msg_type in filter_list:
            print('Filter caught :: {}'.format(msg_type))
            return True

        if 'contain' not in filter_list and 'notcontain' not in filter_list:
            print('All filters passed.')
            return False

        # Assume message does not contain the required word
        contains_required_word = False
        if 'contain' in filter_list:
            # Look for text messages only
            if message_event.media is not None:
                return False
            keywords = filter_dict['contain'].split('<stop_word>')
            for keyword in keywords:
                if keyword in msg_text:
                    contains_required_word = True
                    break

        # Assume message does contain the blacklist word
        contains_blacklist_word = False
        if 'notcontain' in filter_list:
            # Look for text messages only
            if message_event.media is not None:
                return False
            keywords = filter_dict['notcontain'].split('<stop_word>')
            for keyword in keywords:
                if keyword in msg_text:
                    contains_blacklist_word = True
                    break

        print('Contains word :: {} && Contains Blacklist :: {}'.format(
            contains_required_word, contains_blacklist_word))
        return (not contains_required_word) or contains_blacklist_word


if __name__ == "__main__":
    resp = MessageFilter.get_filter('50')
    print(resp)
    filter_list = MessageFilter.get_active_filters(resp)
    print(filter_list)
