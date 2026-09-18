# Campaign Management

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Campaigns

A campaign controls the objective, budget, schedule, and targeting shared by its ad groups. Create the campaign first, then add ad groups and ads.

### Create a campaign

```bash
curl -X POST "https://api.ads.openai.com/v1/campaigns" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Idempotency-Key: campaign-create-001" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Spring launch",
    "status": "paused",
    "bidding_type": "clicks",
    "budget": {
      "daily_spend_limit_micros": 50000000
    },
    "targeting": {
      "locations": {
        "countries": [
          "US"
        ]
      }
    },
    "landing_page_configuration": {
      "query_string_template": "utm_source=openai&utm_medium=paid&utm_campaign={campaign_id}&utm_content={ad_id}"
    }
  }'
```

Save the returned campaign `id`. Set `bidding_type` explicitly: `impressions`, `clicks`, or `conversions`. A conversions campaign also needs an eligible conversion event setting.

### Retrieve and list

```bash
curl -G "https://api.ads.openai.com/v1/campaigns/cmpn_123" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}"
```

Name lookup is exact and case-insensitive and can return multiple matches. Store IDs as the durable identifiers for your integration.

```bash
curl -G "https://api.ads.openai.com/v1/campaigns" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'name=Spring launch'
```

### Update a campaign

```bash
curl -X POST "https://api.ads.openai.com/v1/campaigns/cmpn_123" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Spring launch — updated",
    "budget": {
      "daily_spend_limit_micros": 75000000
    }
  }'
```

Retrieve the current resource before editing nested settings or arrays. Build the complete desired targeting or conversion-event list when changing those fields so you preserve values you intend to keep.

### Change campaign status

Use `POST /v1/campaigns/{campaign_id}/activate`, `/pause`, or `/archive`. For example:

```bash
curl -X POST "https://api.ads.openai.com/v1/campaigns/cmpn_123/pause" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}"
```

A campaign pause prevents its child ads from serving.

## Ad Groups

Ad groups apply a shared bid configuration and context hints to a group of ads.

### Create an ad group

```bash
curl -X POST "https://api.ads.openai.com/v1/ad_groups" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Idempotency-Key: ad-group-create-001" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "cmpn_123",
    "name": "Trail running",
    "status": "paused",
    "context_hints": [
      "Lightweight trail shoes for rocky terrain"
    ],
    "bidding_config": {
      "billing_event_type": "click",
      "strategy": "fixed_bid",
      "max_bid_micros": 2000000
    }
  }'
```

The campaign must belong to the selected ad account. Save the returned `id` for ad creation and future updates. Set the strategy explicitly. Fixed bidding requires `max_bid_micros`; Maximize Results requires omitting it.

### Retrieve and list

```bash
curl -G "https://api.ads.openai.com/v1/ad_groups/adgrp_123" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}"
```

```bash
curl -G "https://api.ads.openai.com/v1/ad_groups" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'campaign_id=cmpn_123' \
  --data-urlencode 'name=Trail running'
```

### Update an ad group

```bash
curl -X POST "https://api.ads.openai.com/v1/ad_groups/adgrp_123" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Trail running — updated",
    "context_hints": [
      "Lightweight trail shoes for rocky terrain",
      "Water-resistant shoes for wet trails"
    ]
  }'
```

`context_hints` replaces the current list. Include every hint you want to keep. Omitting `bidding_config` preserves the current bid configuration; when supplying it, include its required fields.

Use `/activate`, `/pause`, and `/archive` on the ad-group URL to change its state. An active ad group still depends on an active parent campaign and eligible ads.

## Ads & Creative

An ad supplies the content and destination shown to the user. A standard `chat_card` uses your title, body, image, and landing-page URL.

### Upload an image

```bash
curl -X POST "https://api.ads.openai.com/v1/upload" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -F "file=@/path/to/product-image.png"
```

Alternatively, send JSON containing `image_url` to the same endpoint. Use JPEG, PNG, or WebP and provide an image at least 640 × 640 pixels. Save the returned `file_id`.

### Create a chat-card ad

```bash
curl -X POST "https://api.ads.openai.com/v1/ads" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Idempotency-Key: ad-create-001" \
  -H "Content-Type: application/json" \
  -d '{
    "ad_group_id": "adgrp_123",
    "name": "Trail shoe launch",
    "status": "paused",
    "creative": {
      "type": "chat_card",
      "title": "Find your next trail shoe",
      "body": "Explore shoes made for your next outdoor run.",
      "target_url": "https://example.com/trail-shoes",
      "file_id": "file_123"
    }
  }'
```

Use a title of 3–50 characters and a body no longer than 100 characters. The destination must be an HTTP or HTTPS URL no longer than 2,048 characters and accessible to OpenAI's ad crawlers. The file and ad group must belong to the selected account.

### Review and update

```bash
curl -G "https://api.ads.openai.com/v1/ads/ad_123" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}"
```

Inspect `status`, `review_status`, and `review`. Updating creative creates a new submitted version and starts another review:

```bash
curl -X POST "https://api.ads.openai.com/v1/ads/ad_123" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "creative": {
      "type": "chat_card",
      "title": "Ready for your next trail?",
      "body": "Explore our latest trail running collection.",
      "target_url": "https://example.com/trail-shoes",
      "file_id": "file_123"
    }
  }'
```

The example sends the complete intended creative. The ad cannot be moved to another ad group.

Use `/activate`, `/pause`, and `/archive` on the ad to change its state. An active ad still depends on its campaign and ad group.

### Tracking parameters

Add `landing_page_configuration.query_string_template` at the campaign, ad-group, or ad level. For example:

```json
{
  "landing_page_configuration": {
    "query_string_template": "utm_source=openai&utm_campaign={campaign_id}&utm_content={ad_id}&click_id={oppref}"
  }
}
```

Parameters from different levels combine. For a duplicate parameter, precedence is: existing destination URL, ad, ad group, campaign, then ad account.

## Ad Previews

Check the creative, destination, review status, account reviews, targeting, and budget. A preview shows appearance; it does not confirm serving eligibility.

```bash
curl -X POST "https://api.ads.openai.com/v1/ads/ad_123/preview" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}"
```

```bash
curl -G "https://api.ads.openai.com/v1/ads/ad_123" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'include[]=serving_issues'
```

## Bulk Operations

Use a bulk mutation job to create or update many campaigns, ad groups, and ads asynchronously. A job can contain up to 1,000 operations and a request body up to 16 MiB.

### Submit updates

This example validates a campaign budget change and an ad-group pause without applying them. Change `validate_only` to `false` and use a new job key when you are ready to apply the changes.

```bash
curl -X POST "https://api.ads.openai.com/v1/bulk_mutation_jobs" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Idempotency-Key: bulk-validation-001" \
  -H "Content-Type: application/json" \
  -d '{
    "validate_only": true,
    "partial_failure": true,
    "operations": [
      {
        "operation_id": "update-budget",
        "type": "campaign.update",
        "target_resource_id": "cmpn_123",
        "input": {
          "max_budget_micros": 150000000
        }
      },
      {
        "operation_id": "pause-ad-group",
        "type": "ad_group.update",
        "target_resource_id": "adgrp_123",
        "input": {
          "status": "paused"
        }
      }
    ]
  }'
```

A successful submission returns HTTP 202. Save the job ID. The bulk `input` format differs from the single-resource API: for example, the bulk campaign input uses `max_budget_micros`. Do not paste a single-resource body into a bulk operation without checking its schema.

### Create a hierarchy

Supported operation types are `campaign.create`, `campaign.update`, `ad_group.create`, `ad_group.update`, `ad.create`, and `ad.update`.

Each create operation has its own `idempotency_key`. Create an ad group's parent campaign in the same job and reference its key through `campaign_idempotency_key`. An ad also references the same-job parent ad group through `ad_group_idempotency_key`. Each operation needs a unique `operation_id`.

The following validates a complete hierarchy. Substitute your real destination and publicly accessible image URL before applying it:

```bash
curl -X POST "https://api.ads.openai.com/v1/bulk_mutation_jobs" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Idempotency-Key: bulk-hierarchy-validation-001" \
  -H "Content-Type: application/json" \
  -d '{
    "validate_only": true,
    "partial_failure": true,
    "operations": [
      {
        "operation_id": "create-campaign",
        "type": "campaign.create",
        "idempotency_key": "bulk-campaign-001",
        "input": {
          "name": "Catalog launch",
          "max_budget_micros": 100000000,
          "billing_event_type": "click",
          "budget_type": "lifetime",
          "status": "paused",
          "target_countries": [
            "US"
          ]
        }
      },
      {
        "operation_id": "create-ad-group",
        "type": "ad_group.create",
        "idempotency_key": "bulk-ad-group-001",
        "input": {
          "campaign_idempotency_key": "bulk-campaign-001",
          "name": "Trail running",
          "max_bid_micros": 2000000,
          "status": "paused"
        }
      },
      {
        "operation_id": "create-ad",
        "type": "ad.create",
        "idempotency_key": "bulk-ad-001",
        "input": {
          "campaign_idempotency_key": "bulk-campaign-001",
          "ad_group_idempotency_key": "bulk-ad-group-001",
          "title": "Explore trail running shoes",
          "body": "Find your next pair for the trail.",
          "target_url": "https://example.com/trail-shoes",
          "source_image_url": "https://example.com/images/trail-shoes.jpg",
          "status": "paused"
        }
      }
    ]
  }'
```

### Poll the job and read all results

```bash
curl -G "https://api.ads.openai.com/v1/bulk_mutation_jobs/JOB_ID" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}"
```

Wait for `completed`, `partially_failed`, or `failed`. Then retrieve operation outcomes:

```bash
curl -G "https://api.ads.openai.com/v1/bulk_mutation_jobs/JOB_ID/operations" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'limit=100'
```

Results distinguish `created`, `updated`, `validated`, `failed`, and `skipped`. Read every page. After the job finishes, use the last operation's `operation_id` as `after` when `has_more` is true.

### Handle partial failure and retries

With `partial_failure: true`, unrelated operations can continue after a failure. With `false`, remaining operations are skipped after a failure. Neither mode rolls back successful operations. Failed dependencies cause dependent operations to be skipped.

Retry a network-uncertain submission with the same job key and body. The same key with a different body returns a conflict. To retry a finished failed job, follow the operation results, retain create-operation keys, and use a new job key. Respect `retryable` and `retry_after_seconds` when returned.

See the [Bulk API guide](https://developers.openai.com/ads/bulk-api) for additional operation schemas, limits, and examples.