# For the Project Reviewer

## Live Demo

The application is deployed and accessible at:

**🌐 URL: https://tsvtln.com**

---

## Test Account Credentials

Use the following account to log in and explore the platform:

| Field    | Value               |
|----------|---------------------|
| Username | `SoftUni`           |
| Password | `QtvMX28QVL@H1Bq3P` |

> **Note:**  
> This account has full permissions (**is_staff**).  
> To access the Django admin panel, navigate to **https://tsvtln.com/admin/**  
The standard Django admin login is replaced by the site's own login page. 
Log in with the credentials above and you will have access to the Admin panel from the navigation bar as well.

---

## Hosting Infrastructure

| Component           | Details                                                                                                                                                                                                                                                                |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Cloud Provider**  | Microsoft Azure - B2 resource.<br>Lowest cost tier, which is free for students.<br>The only payment required is for the public IP, for easier access to the resource from my workstation.<br>The resources are hardened to avoid malicious connections.                |
| **Domain & Tunnel** | Cloudflare - DNS hosting + Cloudflare Tunnel routing traffic to the Azure resource (no open inbound ports).<br>There is also additional mail routing so that any mail sent to the website's email address (`checkpoint@tsvtln.com`) is forwarded to a dedicated email. |
| **Web Server**      | nginx - reverse proxy in front of the application to handle request routing, serve static assets and improve scalability and performance.                                                                                                                              |
| **App Server**      | Gunicorn - serves the Django application.                                                                                                                                                                                                                              |
| **Task Queue**      | Redis + Celery - used for async task processing and periodic jobs.                                                                                                                                                                                                     |

![azureResource](/docs/_assets/azure_resource.png)

---

<div style="display: flex">
  <a href="../README.md">
    <svg width="20" height="20" fill="blue" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Capa_1" width="800px" height="800px" viewBox="0 0 495.398 495.398" xml:space="preserve">
    <g>
        <g>
            <g>
                <path d="M487.083,225.514l-75.08-75.08V63.704c0-15.682-12.708-28.391-28.413-28.391c-15.669,0-28.377,12.709-28.377,28.391     v29.941L299.31,37.74c-27.639-27.624-75.694-27.575-103.27,0.05L8.312,225.514c-11.082,11.104-11.082,29.071,0,40.158     c11.087,11.101,29.089,11.101,40.172,0l187.71-187.729c6.115-6.083,16.893-6.083,22.976-0.018l187.742,187.747     c5.567,5.551,12.825,8.312,20.081,8.312c7.271,0,14.541-2.764,20.091-8.312C498.17,254.586,498.17,236.619,487.083,225.514z"/>
                <path d="M257.561,131.836c-5.454-5.451-14.285-5.451-19.723,0L72.712,296.913c-2.607,2.606-4.085,6.164-4.085,9.877v120.401     c0,28.253,22.908,51.16,51.16,51.16h81.754v-126.61h92.299v126.61h81.755c28.251,0,51.159-22.907,51.159-51.159V306.79     c0-3.713-1.465-7.271-4.085-9.877L257.561,131.836z"/>
            </g>
        </g>
    </g>
    </svg>
  </a>
 <a style="margin-left: 10px" href="../README.md">Home</a>
</div>

---

