# **NASA API Tools Collection**

### **Description**
The `alta3.nasa_api` collection provides tools to interact with NASA's Astronomy Picture of the Day (APOD) API. This collection includes:
- A custom Ansible module (`apod_module`) for fetching APOD data.
- A role (`apod_downloader`) for downloading APOD images to a specified directory.

### **Included Content**
| **Type**  | **Name**          | **Description**                                      |
|-----------|-------------------|------------------------------------------------------|
| Module    | `apod_module`     | Fetch data from NASA's APOD API, including HD image URLs. |
| Role      | `apod_downloader` | Fetch and download high-definition APOD images to a specified directory. |

### **Requirements**
- Python `requests` library installed on the control node.
- A valid NASA API key for accessing the APOD API.

### **Installation**
To install this collection, run:
```bash
ansible-galaxy collection install git+https://github.com/csfeeser/nasa_api.git
```

---
### README for the **Module**

## alta3.nasa_api.apod – Fetch data from NASA's APOD (Astronomy Picture of the Day) API

### Synopsis

This module interacts with NASA's APOD API to fetch information about astronomical images. It retrieves data such as the `hdurl`, `date`, and `title` of images for a specific date, date range, or randomly selected images.

### Requirements

- Python `requests` library must be installed.
- A valid NASA API key.

### Parameters

| Parameter     | Required | Default  | Choices      | Description                                                                                     |
|---------------|----------|----------|--------------|-------------------------------------------------------------------------------------------------|
| `api_key`     | yes      | None     | N/A          | Your NASA API key.                                                                              |
| `date`        | no       | None     | YYYY-MM-DD   | Specific date to fetch an APOD image.                                                          |
| `start_date`  | no       | None     | YYYY-MM-DD   | Start date for a date range.                                                                   |
| `end_date`    | no       | None     | YYYY-MM-DD   | End date for a date range (used with `start_date`).                                             |
| `count`       | no       | None     | Integer      | Number of random APOD images to fetch. Cannot be used with `date` or `start_date`/`end_date`.  |
| `thumbs`      | no       | False    | `true`, `false` | Include video thumbnails if APOD is a video. Ignored for images.                              |

### Examples

#### Fetch APOD for a Specific Date
```yaml
- name: Fetch APOD for a specific date
  alta3.nasa_api.apod:
    api_key: YOUR_NASA_API_KEY
    date: "2024-11-20"
```

#### Fetch Random APODs
```yaml
- name: Fetch 5 random APOD images
  alta3.nasa_api.apod:
    api_key: YOUR_NASA_API_KEY
    count: 5
```

#### Fetch APODs for a Date Range
```yaml
- name: Fetch APODs for a date range
  alta3.nasa_api.apod:
    api_key: YOUR_NASA_API_KEY
    start_date: "2024-11-01"
    end_date: "2024-11-10"
```

### Return Values

| Key          | Description                              | Returned |
|--------------|------------------------------------------|----------|
| `hdurl`      | URL of the high-definition image.        | Always (if media is an image) |
| `date`       | Date of the APOD.                       | Always |
| `title`      | Title of the APOD.                      | Always |

### Notes

- Only images are included in the result. Videos and other media types are ignored unless `thumbs` is enabled.
- This module raises an error if the API key is invalid or if there is no internet connection.

---

### README for the **Role**

## apod_downloader – Role to Download NASA's Astronomy Picture of the Day (APOD) Images

### Description

The `apod_downloader` role fetches data from NASA's APOD API and downloads high-definition images to a specified directory. This role uses the `apod_module` custom module to interact with the API.

### Requirements

- The `apod_module` custom module must be installed and available in your Ansible environment.
- Python `requests` library must be installed.
- A valid NASA API key.

### Role Variables

| Variable            | Default Value       | Description                                                                               |
|---------------------|---------------------|-------------------------------------------------------------------------------------------|
| `apod_api_key`      | `DEMO_KEY`          | Your NASA API key.                                                                        |
| `apod_count`        | `3`                 | Number of APODs to fetch.                                                                 |
| `apod_download_dir` | `/tmp/apod_images` | Directory where the images will be downloaded.                                            |

### Example Playbook

#### Basic Usage
```yaml
---
- name: Download APOD images
  hosts: localhost
  roles:
    - role: apod_downloader
      vars:
        apod_api_key: YOUR_NASA_API_KEY
        apod_count: 5
        apod_download_dir: /home/student/apod_images
```

### Tasks Included

1. **Ensure Directory Exists**: Creates the target directory if it does not already exist.
2. **Fetch APOD Data**: Uses the `apod_module` to fetch image data from the NASA API.
3. **Download Images**: Downloads high-definition images from the URLs provided by the `apod_module`.

### Notes

- Only high-definition images (`hdurl`) are downloaded. Videos are ignored.
- The images are named with their date and sanitized title for easy identification.
