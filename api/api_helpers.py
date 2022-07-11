"""File holding some reusable methods used in the API addon submission tests"""
import json
import zipfile


def make_addon(manifest_data):
    """Dynamically create a simple extension with minimal manifest properties"""
    with open('sample-addons/manifest.json', 'w') as f:
        # the contents of the manifest will be defined in tests based on the scenario we want to verify
        json.dump(manifest_data, f)
        print(f'Manifest content: {manifest_data}')
    # add the manifest to the addon zip we want to upload - this will always be the 'make-addon.zip' file
    # if the zip files contains a manifest already, it will be overwritten by the new manifest
    with zipfile.ZipFile('sample-addons/make-addon.zip', 'w') as zipf:
        manifest = 'sample-addons/manifest.json'
        destination = 'manifest.json'
        zipf.write(manifest, destination)


def verify_addon_response_details(payload, response, request):
    """Method checking that the values set in the request payload are found
    in the response returned by the API. It can be used both for verifying
    new uploads and addon edits, based on the <request> argument."""
    # save the request values (stored in a dictionary) in a list
    addon_details = [value for value in payload.values()]
    # capture the necessary response values from the JSON response and add them to a list
    response_values = [
        response['categories'],
        response['slug'],
        response['name'],
        response['summary'],
        response['description'],
        response['developer_comments'],
        response['homepage']['url'],
        response['support_email'],
        response['is_experimental'],
        response['requires_payment'],
        response['contributions_url']['url'].split('?')[0],
        response['tags'],
    ]
    # for new uploads, we need to check the version values as well
    if request == 'create':
        # remove the 'upload' value from the request details because it is not present in the JSON response
        addon_details[-1].pop('upload')
        # store the version request details, which are stored in a nested dict inside
        # the 'addon details' dict, in a separate list
        version_details = addon_details[-1].values()
        # remove the dictionary from the 'addon details' initial list
        # and replace it with the individual values stored in the 'version_details' list
        addon_details.pop()
        addon_details.extend([detail for detail in version_details])
        # extend the response values to include the 'current_version' details
        response_values.extend(
            [
                response['current_version']['license']['slug'],
                response['current_version']['release_notes'],
                response['current_version']['compatibility'],
            ]
        )
    print(f'List of request values: {addon_details}')
    print(f'List of response values: {response_values}')
    # compare the request details list with the response details list
    return addon_details == response_values
