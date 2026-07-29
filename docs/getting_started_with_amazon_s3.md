---
title: "Getting started with Amazon S3"
url: "https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html"
service: "AmazonS3"
---

# Getting started with Amazon S3

You can get started with Amazon S3 by working with buckets and objects. A *bucket* is a container for objects. An *object* is
a file and any metadata that describes that file.

To store an object in Amazon S3, you create a bucket and then upload the object to the bucket.
When the object is in the bucket, you can open it, download it, and move it. When you no longer
need an object or a bucket, you can clean up your resources.

With Amazon S3, you pay only for what you use. For more information about Amazon S3 features and
pricing, see [Amazon S3](https://aws.amazon.com/s3). If you are a new Amazon S3 customer, you
can get started with Amazon S3 for free. For more information, see [AWS Free Tier](https://aws.amazon.com/free).

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### Video: Getting started with Amazon S3

The following video shows you how to get started with
Amazon S3.

###### Prerequisites

Before you begin, confirm that you've completed the steps in [Setting up Amazon S3](#setting-up-s3).

## Setting up Amazon S3

When you sign up for AWS, your AWS account is automatically signed up for all services
in AWS, including Amazon S3. You are charged only for the services that you use.

With Amazon S3, you pay only for what you use. For more information about Amazon S3 features and
pricing, see [Amazon S3](https://aws.amazon.com/s3). If you are a new Amazon S3 customer, you
can get started with Amazon S3 for free. For more information, see [AWS Free Tier](https://aws.amazon.com/free).

To set up Amazon S3, use the steps in the following sections.

When you sign up for AWS and set up Amazon S3, you can optionally change the display language
in the AWS Management Console. For more information, see [Changing the language
of the AWS Management Console](https://docs.aws.amazon.com/awsconsolehelpdocs/latest/gsg/getting-started.html#change-language) in the *AWS Management Console Getting Started Guide*.

###### Topics

* [Sign up for an AWS account](#sign-up-for-aws)

### Sign up for an AWS account

To get started with AWS, you need an AWS account. For information about creating an AWS account, see
[Getting started with an AWS account](https://docs.aws.amazon.com//accounts/latest/reference/getting-started.html)
in the *AWS Account Management Reference Guide*.

## Step 1: Create your first S3 bucket

After you sign up for AWS, you're ready to create a bucket in Amazon S3 using the AWS Management Console.
Every object in Amazon S3 is stored in a *bucket*. Before you can
store data in Amazon S3, you must create a bucket.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### Note

You are not charged for creating a bucket. You are charged only for storing objects in the
bucket and for transferring objects in and out of the bucket. The charges that you incur
through following the examples in this guide are minimal (less than $1). For more information
about storage charges, see [Amazon S3
pricing](https://aws.amazon.com/s3/pricing/).

1. Sign in to the AWS Management Console and open the Amazon S3 console at
   <https://console.aws.amazon.com/s3/>.
2. In the navigation bar, choose the name of the currently displayed AWS Region. Next, choose the Region in which you want to create a bucket.

   ###### Note

   * After you create a bucket, you can't change its Region.
   * To minimize latency and costs and address regulatory requirements, choose a Region close to
     you. Objects stored in a Region never leave that Region unless you explicitly transfer them to
     another Region. For a list of Amazon S3 AWS Regions, see [AWS service endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region) in the *Amazon Web Services General Reference*.
3. In the left navigation pane, choose **General purpose buckets**.
4. Choose **Create bucket**. The **Create bucket** page opens.
5. For **Bucket name**, enter a name for your bucket.

   The bucket name must:

   * Be unique within a partition. A partition is a grouping of Regions. AWS currently has
     three partitions: `aws` (commercial Regions), `aws-cn` (China Regions), and
     `aws-us-gov` (AWS GovCloud (US) Regions).
   * Be between 3 and 63 characters long.
   * Consist only of lowercase letters, numbers, periods (`.`), and hyphens
     (`-`). For best compatibility, we recommend that you avoid using periods
     (`.`) in bucket names, except for buckets that are used only for static website
     hosting.
   * Begin and end with a letter or number.
   * For a complete list of bucket-naming rules, see [General purpose bucket naming rules](./bucketnamingrules.html).

   ###### Important

   * After you create the bucket, you can't change its name.
   * Don't include sensitive information in the bucket name. The bucket name is visible in the URLs
     that point to the objects in the bucket.
6. (Optional) Under **General configuration**, you can choose to copy an existing
   bucket's settings to your new bucket. If you don't want to copy the settings of an existing bucket, skip
   to the next step.

   ###### Note

   This option:

   * Isn't available in the AWS CLI and is only available in the Amazon S3 console
   * Doesn't copy the bucket policy from the existing bucket to the new bucket

   To copy an existing bucket's settings, under **Copy settings from existing
   bucket**, select **Choose bucket**. The **Choose bucket**
   window opens. Find the bucket with the settings that you want to copy, and select **Choose
   bucket**. The **Choose bucket** window closes, and the **Create
   bucket** window reopens.

   Under **Copy settings from existing bucket**, you now see the name of the
   bucket that you selected. The settings of your new bucket now match the settings of the bucket that you
   selected. If you want to remove the copied settings, choose **Restore defaults**.
   Review the remaining bucket settings on the **Create bucket** page. If you don't want
   to make any changes, you can skip to the final step.
7. Under **Object Ownership**, to disable or enable ACLs and control
   ownership of objects uploaded in your bucket, choose one of the following
   settings:

   ###### ACLs disabled

   * **Bucket owner enforced (default)** â
     ACLs are disabled, and the bucket owner automatically owns and has full control over every object in the general purpose bucket. ACLs
     no longer affect access permissions to data in the S3 general purpose bucket. The bucket uses policies exclusively to define access control.

     By default, ACLs are disabled. A majority of modern use cases in Amazon S3 no
     longer require the use of ACLs. We recommend that you keep ACLs disabled, except
     in circumstances where you must control access for each object
     individually. For more information, see [Controlling ownership of objects and disabling ACLs for your bucket](./about-object-ownership.html).

   ###### ACLs enabled

   * **Bucket owner preferred** â The bucket owner owns and
     has full control over new objects that other accounts write to the bucket with
     the `bucket-owner-full-control` canned ACL.

     If you apply the **Bucket owner preferred** setting, to
     require all Amazon S3 uploads to include the `bucket-owner-full-control`
     canned ACL, you can [add a
     bucket policy](./ensure-object-ownership.html#ensure-object-ownership-bucket-policy) that allows only object uploads that use this
     ACL.
   * **Object writer** â The AWS account that uploads an
     object owns the object, has full control over it, and can grant other users
     access to it through ACLs.

   ###### Note

   The default setting is **Bucket owner enforced**. To apply the
   default setting and keep ACLs disabled, only the `s3:CreateBucket`
   permission is needed. To enable ACLs, you must have the
   `s3:PutBucketOwnershipControls` permission.
8. Under **Block Public Access settings for this bucket**, choose the
   Block Public Access settings that you want to apply to the bucket.

   By default, all four Block Public Access settings are enabled. We recommend that you
   keep all settings enabled, unless you know that you need to turn off one or more of them
   for your specific use case. For more information about blocking public access, see [Blocking public access to your Amazon S3 storage](./access-control-block-public-access.html).

   ###### Note

   To enable all Block Public Access settings, only the `s3:CreateBucket` permission
   is required. To turn off any Block Public Access settings, you must have the
   `s3:PutBucketPublicAccessBlock` permission.
9. (Optional) By default, **Bucket Versioning** is disabled. Versioning is a means
   of keeping multiple variants of an object in the same bucket. You can use versioning to preserve,
   retrieve, and restore every version of every object stored in your bucket. With versioning, you can
   recover more easily from both unintended user actions and application failures. For more information
   about versioning, see [Retaining multiple versions of objects with S3 Versioning](./Versioning.html).

   To enable versioning on your bucket, choose **Enable**.
10. (Optional) Under **Tags**, you can choose to add tags to your bucket. With
    AWS cost allocation, you can use bucket tags to annotate billing for your use of a bucket. A tag is a
    key-value pair that represents a label that you assign to a bucket. For more information, see [Using cost allocation S3 bucket tags](./CostAllocTagging.html).

    To add a bucket tag, enter a **Key** and optionally a
    **Value** and choose **Add Tag**.
11. To configure **Default encryption**, under **Encryption type**,
    choose one of the following:

    * **Server-side encryption with Amazon S3 managed keys (SSE-S3)**
    * **Server-side encryption with AWS Key Management Service keys (SSE-KMS)**
    * **Dual-layer server-side encryption with AWS Key Management Service (AWS KMS) keys
      (DSSE-KMS)**

      ###### Important

      If you use the SSE-KMS or DSSE-KMS option for your default encryption configuration, you are
      subject to the requests per second (RPS) quota of AWS KMS. For more information about AWS KMS quotas
      and how to request a quota increase, see [Quotas](https://docs.aws.amazon.com/kms/latest/developerguide/limits.html) in
      the *AWS Key Management Service Developer Guide*.

    Buckets and new objects are encrypted by using server-side encryption with Amazon S3 managed keys
    (SSE-S3) as the base level of encryption configuration. For more information about default encryption,
    see [Setting default server-side encryption behavior for Amazon S3 buckets](./bucket-encryption.html). For more information about
    SSE-S3, see [Using server-side encryption with Amazon S3 managed keys (SSE-S3)](./UsingServerSideEncryption.html).

    For more information about using server-side encryption to encrypt your data, see [Protecting data with encryption](./UsingEncryption.html).
12. If you chose **Server-side encryption with AWS Key Management Service keys (SSE-KMS)** or
    **Dual-layer server-side encryption with AWS Key Management Service (AWS KMS) keys (DSSE-KMS)**, do the
    following:

    1. Under **AWS KMS key**, specify your KMS key in one of the following ways:

       * To choose from a list of available KMS keys, choose **Choose from
         your AWS KMS keys**, and choose your
         **KMS key** from the list of available keys.

         Both the AWS managed key (`aws/s3`) and your customer managed keys appear in this
         list. For more information about customer managed keys, see [Customer keys and
         AWS keys](https://docs.aws.amazon.com//kms/latest/developerguide/concepts.html#key-mgmt) in the *AWS Key Management Service Developer Guide*.
       * To enter the KMS key ARN, choose **Enter AWS KMS key
         ARN**, and enter your KMS key ARN in the field that appears.
       * To create a new customer managed key in the AWS KMS console, choose **Create a
         KMS key**.

         For more information about creating an AWS KMS key, see [Creating keys](https://docs.aws.amazon.com//kms/latest/developerguide/create-keys.html) in the *AWS Key Management Service Developer Guide*.

       ###### Important

       You can use only KMS keys that are available in the same AWS Region as the bucket. The
       Amazon S3 console lists only the first 100 KMS keys in the same Region as the bucket. To use a
       KMS key that isn't listed, you must enter your KMS key ARN. If you want to use a KMS key
       that's owned by a different account, you must first have permission to use the key, and then you
       must enter the KMS key ARN. For more information about cross account permissions for KMS keys,
       see [Creating KMS keys that other accounts can use](https://docs.aws.amazon.com//kms/latest/developerguide/key-policy-modifying-external-accounts.html#cross-account-console) in the
       *AWS Key Management Service Developer Guide*. For more information about SSE-KMS, see [Specifying server-side encryption with AWS KMS (SSE-KMS)](./specifying-kms-encryption.html). For more
       information about DSSE-KMS, see [Using dual-layer server-side encryption with AWS KMS keys (DSSE-KMS)](./UsingDSSEncryption.html).

       When you use an AWS KMS key for server-side encryption in Amazon S3, you must
       choose a symmetric encryption KMS key. Amazon S3 supports only symmetric encryption KMS keys and not
       asymmetric KMS keys. For more information, see [Identifying symmetric and
       asymmetric KMS keys](https://docs.aws.amazon.com//kms/latest/developerguide/find-symm-asymm.html) in the *AWS Key Management Service Developer Guide*.
    2. When you configure your bucket to use default encryption with SSE-KMS, you can also use S3 Bucket Keys.
       S3 Bucket Keys lower the cost of encryption by decreasing request traffic from Amazon S3 to AWS KMS. For more
       information, see [Reducing the cost of SSE-KMS with Amazon S3 Bucket Keys](./bucket-key.html). S3 Bucket Keys aren't
       supported for DSSE-KMS.

       By default, S3 Bucket Keys are enabled in the Amazon S3 console. We recommend leaving S3 Bucket Keys enabled to
       lower your costs. To disable S3 Bucket Keys for your bucket, under **Bucket Key**, choose
       **Disable**.
13. (Optional) S3 Object Lock helps protect new objects from being deleted or overwritten. For
    more information, see [Locking objects with Object Lock](./object-lock.html). If you want to enable
    S3 Object Lock, do the following:

    1. Choose **Advanced settings**.

       ###### Important

       Enabling Object Lock automatically enables versioning for the bucket. After you've
       enabled and successfully created the bucket, you must also configure the Object Lock default
       retention and legal hold settings on the bucket's **Properties** tab.
    2. If you want to enable Object Lock, choose
       **Enable**, read the warning that appears, and acknowledge it.

    ###### Note

    To create an Object Lock enabled bucket, you must have the following permissions:
    `s3:CreateBucket`, `s3:PutBucketVersioning`, and
    `s3:PutBucketObjectLockConfiguration`.
14. Choose **Create bucket**.

You've created a bucket in Amazon S3.

###### Next step

To add an object to your bucket, see [Step 2: Upload an object to your bucket](#uploading-an-object-bucket).

## Step 2: Upload an object to your bucket

After creating a bucket in Amazon S3, you're ready to upload an object to the bucket. An object
can be any kind of file: a text file, a photo, a video, and so on.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### To upload an object to a bucket

1. Open the Amazon S3 console at
   <https://console.aws.amazon.com/s3/>.
2. In the **Buckets** list, choose the name of the bucket that you want to
   upload your object to.
3. On the **Objects** tab for your bucket, choose
   **Upload**.
4. Under **Files and folders**, choose **Add
   files**.
5. Choose a file to upload, and then choose **Open.**
6. Choose **Upload**.

You've successfully uploaded an object to your bucket.

###### Next step

To view your object, see [Step 3: Download an object](#accessing-an-object).

## Step 3: Download an object

After you upload an object to a bucket, you can view information about your object and
download the object to your local computer.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

### Using the S3 console

This section explains how to use the Amazon S3 console to download an object from an S3
bucket.

###### Note

* You can download only one object at a time.
* If you use the Amazon S3 console to download an object whose key name ends with a
  period (`.`), the period is removed from the key name of the
  downloaded object. To retain the period at the end of the name of the downloaded
  object, you must use the AWS Command Line Interface (AWS CLI), AWS SDKs, or Amazon S3 REST API.

###### To download an object from an S3 bucket

1. Sign in to the AWS Management Console and open the Amazon S3 console at
   <https://console.aws.amazon.com/s3/>.
2. In the left navigation pane, choose **General purpose buckets** or **Directory buckets**.
3. In the buckets list, choose the name of the bucket that you
   want to download an object from.
4. You can download an object from an S3 bucket in any of the following ways:

   * Select the check box next to the object, and choose
     **Download**. If you want to download the object to a
     specific folder, on the **Actions** menu, choose
     **Download as**.
   * If you want to download a specific version of the object, turn on
     **Show versions** (located next to the search box).
     Select the check box next to the version of the object that you want, and
     choose **Download**. If you want to download the object to
     a specific folder, on the **Actions** menu, choose
     **Download as**.

You've successfully downloaded your object.

###### Next step

To copy and paste your object within Amazon S3, see [Step 4: Copy your object to a folder](#copying-an-object).

## Step 4: Copy your object to a folder

You've already added an object to a bucket and downloaded the object. Now, you create a
folder and copy the object and paste it into the folder.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### To copy an object to a folder

1. In the **Buckets** list, choose your bucket name.
2. Choose **Create folder** and configure a new folder:

   1. Enter a folder name (for example, `favorite-pics`).
   2. For the folder encryption setting, choose **Disable**.
   3. Choose **Save**.
3. Navigate to the Amazon S3 bucket or folder that contains the objects that you want to
   copy.
4. Select the check box to the left of the names of the objects that you want to
   copy.
5. Choose **Actions** and choose **Copy** from the list
   of options that appears.

   Alternatively, choose **Copy** from the options that appear.
6. Choose the destination folder:

   1. Choose **Browse S3**.
   2. Choose the option button to the left of the folder name.

      To navigate into a folder and choose a subfolder as your destination, choose the
      folder name.
   3. Choose **Choose destination**.

   The path to your destination folder appears in the **Destination** box.
   In **Destination**, you can alternately enter your destination path, for
   example,
   s3://`bucket-name`/`folder-name`/.
7. Choose **Copy**.

   Amazon S3 copies your objects to the destination folder.

###### Next step

To delete an object and a bucket in Amazon S3, see [Step 5: Delete your objects and bucket](#deleting-object-bucket).

## Step 5: Delete your objects and bucket

When you no longer need an object or a bucket, we recommend that you delete them to prevent
further charges. If you completed this getting started walkthrough as a learning exercise, and
you don't plan to use your bucket or objects, we recommend that you delete your bucket and
objects so that charges no longer accrue.

Before you delete your bucket, empty the bucket or delete the objects in the bucket. After
you delete your objects and bucket, they are no longer available.

If you want to continue to use the same bucket name, we recommend that you delete the
objects or empty the bucket, but don't delete the bucket. After you delete a bucket, the name
becomes available to reuse. However, another AWS account might create a bucket with the same
name before you have a chance to reuse it.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### Topics

* [Deleting an object](#clean-up-delete-objects)
* [Emptying your bucket](#clean-up-empty-bucket)
* [Deleting your bucket](#clean-up-delete-bucket)

### Deleting an object

If you want to choose which objects you delete without emptying all the objects from your
bucket, you can delete an object.

1. In the **Buckets** list, choose the name of the bucket that you want
   to delete an object from.
2. Select the object that you want to
   delete.
3. Choose **Delete** from the options that appear.
4. On the **Delete objects** page, type `delete` to confirm deletion of your objects.
5. Choose **Delete objects**.

### Emptying your bucket

If you plan to delete your bucket, you must first empty your bucket, which deletes all the
objects in the bucket.

###### To empty a bucket

1. In the **Buckets** list, select the bucket that you want to empty,
   and then choose **Empty**.
2. To confirm that you want to empty the bucket and delete all the objects in it, in
   **Empty bucket**, type `permanently
   delete`.

   ###### Important

   Emptying the bucket cannot be undone. Objects added to the bucket while the empty
   bucket action is in progress will be deleted.
3. To empty the bucket and delete all the objects in it, and choose
   **Empty**.

   An **Empty bucket: Status** page opens that you can use to review a
   summary of failed and successful object deletions.
4. To return to your bucket list, choose **Exit**.

### Deleting your bucket

After you empty your bucket or delete all the objects from your bucket, you can delete
your bucket.

1. To delete a bucket, in the **Buckets** list, select the
   bucket.
2. Choose **Delete**.
3. To confirm deletion, in **Delete bucket**, type the name of the
   bucket.

   ###### Important

   Deleting a bucket cannot be undone. Bucket names are unique. If you delete your
   bucket, another AWS user can use the name. If you want to continue to use the same
   bucket name, don't delete your bucket. Instead, empty and keep the bucket.
4. To delete your bucket, choose **Delete bucket**.

## Next steps

In the preceding examples, you learned how to perform some basic Amazon S3 tasks.

The following topics explain the learning paths that you can use to
gain a deeper understanding of Amazon S3 so that you can implement it in your
applications.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### Topics

* [Understand common use cases](#s3-use-cases)
* [Control access to your buckets and objects](#control-access-resources)
* [Protect and monitor your storage](#manage-monitor-storage)
* [Develop with Amazon S3](#develop-with-s3)
* [Learn from tutorials](#s3-getting-started-tutorials-list)
* [Explore training and support](#explore-training-and-support)

### Understand common use cases

You can use Amazon S3 to support your specific use case. The [AWS Solutions
Library](https://aws.amazon.com/solutions/) and [AWS
Blog](https://aws.amazon.com/blogs/) provide use-case specific information and
tutorials. The following are some common use cases for Amazon S3:

* Backup and storage â Use Amazon S3 storage
  management features to manage costs, meet regulatory requirements, reduce
  latency, and save multiple distinct copies of your data for compliance
  requirements.
* Application hosting â Deploy, install,
  and manage web applications that are reliable, highly scalable, and low-cost.
  For example, you can configure your Amazon S3 bucket to host a static website. For
  more information, see [Hosting a static website using Amazon S3](./WebsiteHosting.html).
* Media hosting â Build a highly available
  infrastructure that hosts video, photo, or music uploads and downloads.
* Software delivery â Host your software
  applications for customers to download.

### Control access to your buckets and objects

Amazon S3 provides a variety of security features and tools. For an overview, see [Access control in Amazon S3](./access-management.html).

By default, S3 buckets and the objects in them are private. You
have access only to the S3 resources that you create. You can use
the following features to grant granular resource permissions that
support your specific use case or to audit the permissions of your
Amazon S3 resources.

* [S3
  Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html) â Block public access to S3 buckets and
  objects. By default, Block Public Access settings are turned on at the bucket
  level.
* [AWS Identity and Access Management (IAM)
  identities](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-iam.html) â Use IAM or AWS IAM Identity Center to create IAM
  identities in your AWS account to manage access to your Amazon S3 resources. For
  example, you can use IAM with Amazon S3 to control the type of access that a user
  or group of users has to an Amazon S3 bucket that your AWS account owns. For more
  information about IAM identities and best practices, see [IAM identities
  (users, user groups, and roles)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id.html) in the *IAM User Guide*.
* [Bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html) â Use IAM-based policy
  language to configure resource-based permissions for your S3
  buckets and the objects in them.
* [Access
  control lists (ACLs)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/acls.html) â Grant read and write permissions for
  individual buckets and objects to authorized users. As a general rule, we
  recommend using S3 resource-based policies (bucket policies and access point
  policies) or IAM user policies for access control instead of ACLs. Policies
  are a simplified and more flexible access-control option. With bucket policies
  and access point policies, you can define rules that apply broadly across all
  requests to your Amazon S3 resources. For more information about the specific cases
  when you'd use ACLs instead of resource-based policies or IAM user policies,
  see [Identity and Access Management for Amazon S3](./security-iam.html).
* [S3 Object Ownership](https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html) â Take ownership of every object in
  your bucket, simplifying access management for data stored in Amazon S3.
  S3 Object Ownership is an Amazon S3 bucket-level setting that you can use to
  disable or enable ACLs. By default, ACLs are disabled. With ACLs disabled, the
  bucket owner owns all the objects in the bucket and manages access to data
  exclusively by using access-management policies.
* [IAM Access Analyzer for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-analyzer.html) â Evaluate and monitor your S3
  bucket access policies, ensuring that the policies provide
  only the intended access to your S3 resources.

### Protect and monitor your storage

* [Protecting your storage](./data-protection.html) â After
  you create buckets and upload objects in Amazon S3, you can protect your object
  storage. For example, you can use S3 Versioning, S3 Replication, and Multi-Region Access Point
  failover controls for disaster recovery, AWS Backup to back up your data, and
  S3 Object Lock to set retention periods, prevent deletions and overwrites, and
  meet compliance requirements.
* [Monitoring your
  storage](./monitoring-overview.html) â Monitoring is an important part
  of maintaining the reliability, availability, and
  performance of Amazon S3 and your AWS solutions. You can
  monitor storage activity and costs. Also, we recommend that
  you collect monitoring data from all the parts of your AWS
  solution so that you can more easily debug a multipoint
  failure if one occurs.

  You can also use analytics and insights in Amazon S3 to understand, analyze, and
  optimize your storage usage. For example, use [Amazon S3 Storage Lens](./storage_lens.html) to understand, analyze, and optimize your storage.
  S3 Storage Lens provides 29+ usage and activity metrics and interactive dashboards to
  aggregate data for your entire organization, specific accounts, Regions,
  buckets, or prefixes. Use [Storage Class
  Analysis](./analytics-storage-class.html) to analyze storage access patterns to decide when it's time
  to move your data to a more cost-effective storage class. To manage your costs,
  you can use [S3 Lifecycle](./object-lifecycle-mgmt.html).

### Develop with Amazon S3

Amazon S3 is a REST service. You can send requests to Amazon S3 using the
REST API or the AWS SDK libraries, which wrap the underlying Amazon S3
REST API, simplifying your programming tasks. You can also use the
AWS Command Line Interface (AWS CLI) to make Amazon S3 API calls. For more information, see
[Making requests](https://docs.aws.amazon.com/AmazonS3/latest/API/MakingRequests.html) in the *Amazon S3 API Reference*.

The Amazon S3 REST API is an HTTP interface to Amazon S3. With the REST API,
you use standard HTTP requests to create, fetch, and delete buckets
and objects. To use the REST API, you can use any toolkit that
supports HTTP. You can even use a browser to fetch objects, as long
as they are anonymously readable. For more information, see [Developing with Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/API/developing-s3.html) in the *Amazon S3 API Reference*.

To help you build applications using the language of your choice, we provide the
following resources.

###### AWS CLI

You can access the features of Amazon S3 using the AWS CLI.
To download and configure the AWS CLI, see [Developing with Amazon S3 using the AWS CLI](https://docs.aws.amazon.com/AmazonS3/latest/API/setup-aws-cli.html) in the *Amazon S3 API Reference*.

The AWS CLI provides two tiers of commands for accessing
Amazon S3: High-level ([s3](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html)) commands and API-level ([s3api](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-apicommands.html) and `s3control` commands. The high-level S3
commands simplify performing common tasks, such as
creating, manipulating, and deleting objects and
buckets. The s3api and s3control commands expose direct
access to all Amazon S3 API operations, which you can use to
carry out advanced operations that might not be possible
with the high-level commands alone.

For a list of Amazon S3 AWS CLI commands, see [s3](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/index.html), [s3api](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/index.html), and [s3control](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3control/index.html).

###### AWS SDKs and Explorers

You can use the AWS SDKs when developing applications with Amazon S3. The
AWS SDKs simplify your programming tasks by wrapping the underlying REST
API. The AWS Mobile SDKs and the Amplify JavaScript library are also
available for building connected mobile and web applications using
AWS.

In addition to the AWS SDKs, AWS Explorers are
available for Visual Studio and Eclipse for Java IDE. In
this case, the SDKs and the explorers are bundled
together as AWS Toolkits.

For more information, see [Developing with Amazon S3 using the AWS SDKs](https://docs.aws.amazon.com/AmazonS3/latest/API/sdk-general-information-section.html) in the *Amazon S3 API Reference*.

###### Sample Code and Libraries

The [AWS
Developer Center](https://aws.amazon.com/code/Amazon-S3) and [AWS
Code Sample Catalog](https://docs.aws.amazon.com/code-samples/latest/catalog/welcome.html) have sample code and
libraries written especially for Amazon S3. You can use these
code samples to understand how to implement the Amazon S3
API. You can also view the [*Amazon Simple Storage Service API Reference*](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html)
to understand the Amazon S3 API operations in detail.

### Learn from tutorials

You can get started with step-by-step tutorials to learn more about Amazon S3. These tutorials are intended for a lab-type
environment, and they use fictitious company names, user names, and so
on. Their purpose is to provide general guidance. They are not intended
for direct use in a production environment without careful review and
adaptation to meet the unique needs of your organization's environment.

#### Getting started

* [Tutorial: Storing and retrieving a file with Amazon S3](https://aws.amazon.com/getting-started/hands-on/backup-files-to-amazon-s3/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Getting started using S3 Intelligent-Tiering](https://aws.amazon.com/getting-started/hands-on/getting-started-using-amazon-s3-intelligent-tiering/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Getting started using the S3 Glacier storage classes](https://aws.amazon.com/getting-started/hands-on/getting-started-using-amazon-s3-glacier-storage-classes/?ref=docs_gateway/amazons3/tutorials.html)

#### Optimizing storage costs

* [Tutorial: Getting started using S3 Intelligent-Tiering](https://aws.amazon.com/getting-started/hands-on/getting-started-using-amazon-s3-intelligent-tiering/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Getting started using the S3 Glacier; storage classes](https://aws.amazon.com/getting-started/hands-on/getting-started-using-amazon-s3-glacier-storage-classes/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Optimizing costs and gaining visibility into usage with S3 Storage Lens](https://aws.amazon.com/getting-started/hands-on/amazon-s3-storage-lens/?ref=docs_gateway/amazons3/tutorials.html)

#### Managing storage

* [Tutorial: Getting started with Amazon S3 Multi-Region Access Points](https://aws.amazon.com/getting-started/hands-on/getting-started-with-amazon-s3-multi-region-access-points/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Replicating existing objects in your Amazon S3 buckets with S3 Batch Replication](https://aws.amazon.com/getting-started/hands-on/replicate-existing-objects-with-amazon-s3-batch-replication/?ref=docs_gateway/amazons3/tutorials.html)

#### Hosting videos and websites

* [Tutorial: Hosting on-demand streaming video with Amazon S3, Amazon CloudFront, and Amazon RouteÂ 53](./tutorial-s3-cloudfront-route53-video-streaming.html)
* [Tutorial: Configuring a static website on Amazon S3](./HostingWebsiteOnS3Setup.html)
* [Tutorial: Configuring a static website using a custom domain registered with RouteÂ 53](./website-hosting-custom-domain-walkthrough.html)

#### Processing data

* [Tutorial: Transforming data for your application with S3 Object Lambda](./tutorial-s3-object-lambda-uppercase.html)
* [Tutorial: Detecting and redacting PII data with S3 Object Lambda and Amazon Comprehend](./tutorial-s3-object-lambda-redact-pii.html)
* [Tutorial: Using S3 Object Lambda to dynamically watermark images as they are retrieved](https://aws.amazon.com/getting-started/hands-on/amazon-s3-object-lambda-to-dynamically-watermark-images/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Batch-transcoding videos with S3 Batch Operations](./tutorial-s3-batchops-lambda-mediaconvert-video.html)

#### Protecting data

* [Tutorial: Checking the integrity of data in Amazon S3 with additional checksums](https://aws.amazon.com/getting-started/hands-on/amazon-s3-with-additional-checksums/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Replicating data within and between AWS Regions using S3 Replication](https://aws.amazon.com/getting-started/hands-on/replicate-data-using-amazon-s3-replication/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Protecting data on Amazon S3 against accidental deletion or application bugs
  using S3 Versioning, S3 Object Lock, and S3 Replication](https://aws.amazon.com/getting-started/hands-on/protect-data-on-amazon-s3/?ref=docs_gateway/amazons3/tutorials.html)
* [Tutorial: Replicating existing objects in your Amazon S3 buckets with S3 Batch Replication](https://aws.amazon.com/getting-started/hands-on/replicate-existing-objects-with-amazon-s3-batch-replication/?ref=docs_gateway/amazons3/tutorials.html)

### Explore training and support

You can learn from AWS experts to advance your skills and get expert assistance
achieving your objectives.

* Training â Training resources provide a hands-on approach to learning Amazon S3. For more
  information, see [AWS training and
  certification](https://www.aws.training) and [AWS online tech talks](https://aws.amazon.com/events/online-tech-talks).
* Discussion Forums â On the forum, you can review posts to understand what you can and can't do
  with Amazon S3. You can also post your questions. For more information, see
  [Discussion Forums](https://forums.aws.amazon.com/index.jspa).
* Technical Support â If you have further questions, you can contact [Technical Support](https://aws.amazon.com/contact-us).

[Document Conventions](/general/latest/gr/docconventions.html)

Amazon S3 Object Lambda availability change

Using Amazon S3 with the AWS CLI